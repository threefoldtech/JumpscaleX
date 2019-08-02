import os
from concurrent.futures import ThreadPoolExecutor, wait
import requests
from configparser import ConfigParser
from Jumpscale.tools.googleslides.slides2html.google_links_utils import get_slide_id, get_presentation_id, link_info
from Jumpscale import j

# logging.basicConfig()
# logger = logging.getLogger('downloader')

# The ID template for google presentation.
DOWNLOAD_SLIDE_AS_JPEG_TEMPLATE = (
    "https://docs.google.com/presentation/d/{presentationId}/export/jpeg?id={presentationId}&pageid={pageId}"
)


def download_one(url, destfile):
    r = requests.get(url)
    if r.status_code == 200 and not os.path.exists(destfile):
        with open(destfile, "wb") as f:
            content = r.content
            f.write(content)


def download_entry(entry, destdir="/tmp"):
    """Download single entry

    Arguments:
        entry: Tuple -- (url, save_as, slide_meta, presentation_title)

    Keyword Arguments:
        destdir {str} -- destination directory (default: {"/tmp"})

    Returns:
        string -- [destination file to download]
    """

    url, save_as, slide_meta, slide_title, presentation_title = entry
    destfile = os.path.join(destdir, save_as)

    print("Downloading {} to {}".format(url, destfile))
    metapath = destfile + ".meta"
    print("Metapath: ", metapath)
    with open(metapath, "w") as f:
        f.write("".join(slide_meta))

    download_one(url, destfile)

    return destfile


def download_entries(entries, destdir="/tmp"):
    """Download slides to destination website directory

    Arguments:
        entries List[(url, save_as, slide_meta, presentation_title)] -- [description]

    Keyword Arguments:
        destdir {str} -- [description] (default: {"/tmp"})
    """

    results = []
    os.makedirs(destdir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for entry in entries:
            future = executor.submit(download_entry, entry, destdir)
            results.append(future)
    wait(results)


class Downloader:
    def __init__(self, presentation_id, service, thumbnailsize="MEDIUM"):
        """
        Download class responsible for downloading slides as images
        Arguments:
            presentation_id {str} -- presentation id from google presentation id
            service {Service} -- Google api service (created by build)
            thumbnailsize {str} -- image size (medium or large)
        """

        self.presentation_id = presentation_id
        self.service = service
        self.thumbnailsize = thumbnailsize.upper()  # "LARGE."
        if thumbnailsize not in ["MEDIUM", "LARGE"]:
            raise j.exceptions.Value("invalid thumbnailsize should be large or medium")

    def _get_slides_download_info(self):
        presentation = self.service.presentations().get(presentationId=self.presentation_id).execute()
        presentation_title = presentation["title"]
        slides = presentation.get("slides")
        slides_ids = [slide["objectId"] for slide in slides]

        links = []
        zerofills = len(str(len(slides)))
        for i, slide_id in enumerate(slides_ids):
            # slide_index = slide_id.split("_")[2]
            slide = slides[i]
            slide_meta = []
            notesPage = slide["slideProperties"]["notesPage"]
            # speakerNotesObjectId = notesPage['notesProperties']['speakerNotesObjectId'] #i3

            pageElements = notesPage["pageElements"]
            slide_title = None
            for page_element in pageElements:
                # if page_element['objectId'] == speakerNotesObjectId:
                shape = page_element["shape"]
                if "text" in shape and "textElements" in shape["text"]:
                    for text_element in shape["text"]["textElements"]:
                        if "textRun" in text_element and "content" in text_element["textRun"]:
                            slide_meta.append(text_element["textRun"]["content"])
                            if not slide_title:
                                slide_title = self._slide_title_get(text_element["textRun"]["content"])
            pageId = slide_id
            presentationId = self.presentation_id
            url = (
                self.service.presentations()
                .pages()
                .getThumbnail(
                    presentationId=presentationId,
                    pageObjectId=pageId,
                    thumbnailProperties_thumbnailSize=self.thumbnailsize,
                )
                .execute()["contentUrl"]
            )
            image_id = str(i).zfill(zerofills)
            save_as = "{image_id}_{page_id}.png".format(image_id=image_id, page_id=pageId)
            links.append((url, save_as, slide_meta, slide_title, presentation_title))
        return links, presentation_title

    def _slide_title_get(self, txt):
        for line in txt.split("\n"):
            if line.casefold().startswith("title"):
                parts = line.split("=")
                if len(parts) == 2:
                    return parts[1].strip()
        return None

    def get_background(self, slidelink, destdir):
        presentation_id, background_slide_id = link_info(slidelink)

        if not background_slide_id:
            raise j.exceptions.Value("invalid slide link")
        presentation = self.service.presentations().get(presentationId=presentation_id).execute()
        presentation_title = presentation["title"]
        slides = presentation.get("slides")
        slides_ids = [slide["objectId"] for slide in slides]

        links = []
        zerofills = len(str(len(slides)))

        if len(background_slide_id) < 5:
            background_slide_id = slides_ids[0]

        for i, slide_id in enumerate(slides_ids):
            if slide_id != background_slide_id:
                continue
            else:
                slide = slides[i]
                slide_meta = []
                notesPage = slide["slideProperties"]["notesPage"]
                # speakerNotesObjectId = notesPage['notesProperties']['speakerNotesObjectId'] #i3

                pageElements = notesPage["pageElements"]
                for page_element in pageElements:
                    # if page_element['objectId'] == speakerNotesObjectId:
                    shape = page_element["shape"]
                    if "text" in shape and "textElements" in shape["text"]:
                        for text_element in shape["text"]["textElements"]:
                            if "textRun" in text_element and "content" in text_element["textRun"]:
                                slide_meta.append(text_element["textRun"]["content"])
                pageId = slide_id
                presentationId = presentation_id
                url = (
                    self.service.presentations()
                    .pages()
                    .getThumbnail(
                        presentationId=presentationId,
                        pageObjectId=pageId,
                        thumbnailProperties_thumbnailSize=self.thumbnailsize,
                    )
                    .execute()["contentUrl"]
                )
                image_id = str(i).zfill(zerofills)
                save_as = "background_{image_id}_{page_id}.png".format(image_id=image_id, page_id=pageId)
                save_as_path = os.path.join(destdir, save_as)
                download_one(url, save_as_path)
                return save_as_path

    def download(self, destdir):
        """Download images of self.presentation_id to destination dir

        Arguments:
            destdir {str} -- destination dir.
        """
        entries, title = self._get_slides_download_info()

        parser = ConfigParser()

        website_dir = os.path.dirname(destdir)
        presentations_meta_path = os.path.join(website_dir, "presentations.meta")

        if os.path.exists(presentations_meta_path):
            parser.read(presentations_meta_path)
        if not parser.has_section(self.presentation_id):
            parser.add_section(self.presentation_id)
        parser.set(self.presentation_id, "title", title)
        with open(presentations_meta_path, "w") as metafile:
            parser.write(metafile)

        download_entries(entries, destdir)
        presentations_meta_path = "{}/{}".format(destdir, "presentations.meta.json")
        if not j.sal.fs.exists(presentations_meta_path):
            j.data.serializers.json.dump(presentations_meta_path, {})
        presentation_meta = {}
        for entry in entries:
            _, save_as, _, slide_title, _ = entry
            if slide_title:
                presentation_meta[slide_title] = save_as

        meta = j.data.serializers.json.load(presentations_meta_path)
        meta[self.presentation_id] = presentation_meta
        j.data.serializers.json.dump(presentations_meta_path, meta)
        print("done downloading.")
        return (entries, destdir)
