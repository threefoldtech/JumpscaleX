from Jumpscale import j

class SlideShow:
    def __init__(self):
        self.slides = []

    def slide_add(self, name, presentation_guid, footer, order):
        self.slides.append(Slide(name, presentation_guid, footer, order))

    def slides_get(self):
        return sorted(self.slides, key=lambda slide: slide.order)


class Slide:
    def __init__(self, name, presentation_guid, footer, order):
        self.name = name
        self.presentation_guid = presentation_guid
        self.footer = footer
        self.order = order

def slideshow(doc, **kwargs):
    def _content_parse(content):
        data = dict()
        for line in content.splitlines():
            if "=" in line:
                parts = line.split("=", maxsplit=1)
                key = parts[0].strip()
                value = parts[1].strip()
                data[key] = value
        return data

    slides = SlideShow()
    presentation_guids = {}
    data = _content_parse(kwargs['content'])
    for key, value in data.items():
        if key.casefold().startswith("presentation"):
            presentation_guids[key.strip()] = value

        elif key.casefold().startswith("slide"):
            footer = ""

            if j.data.types.list.check(data[key]) and len(data[key]) > 1:
                footer = data[key][1]
                slide_args = data[key][0]
            else:
                slide_args = data[key]
            slide_num = key.split("_")[1].strip()
            presentation_name = slide_args.split('[')[0]
            slide_name = slide_args.split('[')[1].split(']')[0]
            if slide_name.startswith('id'):
                slide_name = slide_name[3:]
            slides.slide_add(slide_name, presentation_guids[presentation_name], footer, slide_num)

    output = "```slideshow\n"
    for slide in slides.slides_get():
        image_tag = '<img src="/gdrive/slide/{presentation_guid}/{slide_name}" alt="{slide_name}" />'.format(
            presentation_guid=slide.presentation_guid, slide_name=slide.name)
        output += """
            <section>
               <div class="slide-image">
                   {image}
                   <div style="font-size: 200%;">
                   {footer}
                   </div>
               </div>
            </section>""".format(image=image_tag, footer=slide.footer)
    output += "\n```"
    return output

