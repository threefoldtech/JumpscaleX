import inspect

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.completion import Completion
from prompt_toolkit.filters import is_done
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import ConditionalContainer, Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.lexers import PygmentsLexer
from ptpython.filters import ShowDocstring, PythonInputFilter
from ptpython.prompt_style import PromptStyle
from ptpython.utils import get_jedi_script_from_document
from pygments.lexers import PythonLexer


HIDDEN_PREFIXES = ('_', '__')


class KosmosShellConfig():

    pass


def get_object(tbc, locals_=None, globals_=None, walkback=False):
    """
    tries starting from the string e.g. j.clients.ssh to get to an object out of the stack
    :param tbc: the line on the console = text before cursor
    :param locals_:
    :param globals_:
    :param walkback:
    :return:
    """

    j = KosmosShellConfig.j

    try:
        obj = eval(tbc)
        return obj
    except Exception as e:
        # print(e)
        pass

    tbc2 = tbc.split(".")[0]  # e.g. ssh.a becomes ssh, because I need to find the ssh object in the stack

    obj = None
    frame_ = inspect.currentframe()
    if locals_ is None:
        locals_ = frame_.f_locals
        locals_ = j._locals_get(locals_)

    if tbc2 in locals_:
        obj = locals_[tbc2]

    if not obj:

        if not globals_:
            globals_ = frame_.f_back.f_globals

        if tbc2 in globals_:
            obj = globals_[tbc2]

    if not obj:

        if walkback:
            # now walk up to the frames
            while obj is None and frame_:
                locals_ = frame_.f_locals

                if tbc2 in locals_:
                    obj = locals_[tbc2]
                else:
                    frame_ = frame_.f_back

    if "." in tbc:
        tbc3 = ".".join(tbc.split(".")[1:])
        try:
            obj2 = eval("obj.%s" % tbc3)
            return obj2
        except:
            return
    return obj


def sort_members_key(name):
    """Sort members of an object

    :param name: name
    :type name: str
    :return: the order of sorting
    :rtype: int
    """
    if name.startswith('__'):
        return 3
    elif name.startswith('_'):
        return 2
    elif name.isupper():
        return 1
    else:
        return 0


def filter_completions_on_prefix(completions, prefix=''):
    for completion in completions:
        text = completion.text
        if prefix not in HIDDEN_PREFIXES and text.startswith(HIDDEN_PREFIXES):
            continue
        yield completion


def get_current_line(document):
    tbc = document.current_line_before_cursor
    if tbc:
        line = tbc.split('.')
        parent, member = '.'.join(line[:-1]), line[-1]
        if member.startswith('__'):  # then we want to show private methods
            prefix = '__'
        elif member.startswith('_'):  # then we want to show private methods
            prefix = '_'
        else:
            prefix = ''
        return parent, member, prefix
    raise ValueError('nothing is written')


def get_completions(self, document, complete_event):
    """
    get completions for j objects (using _method_) and others (using dir)

    :rtype: `Completion` generator
    """

    def colored_completions(names, color):
        for name in names:
            if not name:
                continue
            if name.startswith(member):
                completion = name[len(member):]
                yield Completion(completion, 0,
                    display=name, style='bg:%s fg:ansiblack' % color,
                    selected_style='bg:ansidarkgray')

    try:
        parent, member, prefix = get_current_line(document)
    except ValueError:
        return

    obj = get_object(parent, self.get_locals(), self.get_globals())
    if obj:
        if hasattr(obj.__class__, '_methods_'):
            yield from colored_completions(obj._properties_children(), 'ansigreen')
            yield from colored_completions(obj._properties_model(), 'ansiyellow')
            yield from colored_completions(obj._methods(prefix=prefix), 'ansiblue')
            yield from colored_completions(obj._properties(prefix=prefix), 'ansigray')
        else:
            # try dir()
            members = sorted(dir(obj), key=sort_members_key)
            yield from colored_completions(members, 'ansigray')


def get_doc_string(tbc):
    j = KosmosShellConfig.j
    obj = get_object(tbc, locals_=None, globals_=None, walkback=True)
    if not obj:
        return

    signature = ''
    try:
        signature = inspect.signature(obj)
        signature = obj.__name__  + str(signature)
    except (ValueError, TypeError):
        # no signature can be provided or it's not supported e.g.
        # a built-in functions or not a module/class/function...
        pass

    doc = inspect.getdoc(obj) or ''
    if not signature:
        return doc
    return '\n\n'.join([signature, doc])


class HasDocString(PythonInputFilter):

    def __call__(self):
        return len(self.python_input.docstring_buffer.text) > 0


class IsInsideString(PythonInputFilter):

    def __call__(self):
        text = self.python_input.default_buffer.document.text_before_cursor
        grammer = self.python_input._completer._path_completer_grammar
        return bool(grammer.match(text))


def setup_docstring_containers(repl):
    # see ptpython.layout
    parent_container = repl.app.layout.container.children[0].children[0]
    # remove ptpython docstring containers, we have ours now
    parent_container.children = parent_container.children[:-2]

    # the same as ptpython containers, but without signature checking
    parent_container.children.extend([
        ConditionalContainer(
            content=Window(
                height=Dimension.exact(1),
                char='\u2500',
                style='class:separator'),
            filter=HasDocString(repl) & ShowDocstring(repl) & ~is_done),
        ConditionalContainer(
            content=Window(
                BufferControl(
                    buffer=repl.docstring_buffer,
                    lexer=PygmentsLexer(PythonLexer),
                ),
                height=Dimension(max=12)),
            filter=HasDocString(repl) & ShowDocstring(repl) & ~is_done),
    ])


def ptconfig(repl):
    repl.exit_message = "We hope you had fun using te kosmos shell"
    repl.show_docstring = True

    # When CompletionVisualisation.POP_UP has been chosen, use this
    # scroll_offset in the completion menu.
    repl.completion_menu_scroll_offset = 0

    # Show line numbers (when the input contains multiple lines.)
    repl.show_line_numbers = True

    # Show status bar.
    repl.show_status_bar = False

    # When the sidebar is visible, also show the help text.
    # repl.show_sidebar_help = True

    # Highlight matching parethesis.
    repl.highlight_matching_parenthesis = True

    # Line wrapping. (Instead of horizontal scrolling.)
    repl.wrap_lines = True

    # Mouse support.
    repl.enable_mouse_support = True

    # Complete while typing. (Don't require tab before the
    # completion menu is shown.)
    # repl.complete_while_typing = True

    # Vi mode.
    repl.vi_mode = False

    # Paste mode. (When True, don't insert whitespace after new line.)
    repl.paste_mode = False

    # Use the classic prompt. (Display '>>>' instead of 'In [1]'.)
    repl.prompt_style = 'classic'  # 'classic' or 'ipython'

    # Don't insert a blank line after the output.
    repl.insert_blank_line_after_output = False

    # History Search.
    # When True, going back in history will filter the history on the records
    # starting with the current input. (Like readline.)
    # Note: When enable, please disable the `complete_while_typing` option.
    #       otherwise, when there is a completion available, the arrows will
    #       browse through the available completions instead of the history.
    # repl.enable_history_search = False

    # Enable auto suggestions. (Pressing right arrow will complete the input,
    # based on the history.)
    repl.enable_auto_suggest = True

    # Enable open-in-editor. Pressing C-X C-E in emacs mode or 'v' in
    # Vi navigation mode will open the input in the current editor.
    # repl.enable_open_in_editor = True

    # Enable system prompt. Pressing meta-! will display the system prompt.
    # Also enables Control-Z suspend.
    repl.enable_system_bindings = False

    # Ask for confirmation on exit.
    repl.confirm_exit = False

    # Enable input validation. (Don't try to execute when the input contains
    # syntax errors.)
    # repl.enable_input_validation = True

    # Use this colorscheme for the code.
    repl.use_code_colorscheme('perldoc')

    # Set color depth (keep in mind that not all terminals support true color).
    repl.color_depth = 'DEPTH_24_BIT'  # True color.

    repl.enable_syntax_highlighting = True

    repl.min_brightness = 0.3

    # Add custom key binding for PDB.

    @repl.add_key_binding(Keys.ControlB)
    def _debug_event(event):
        ' Pressing Control-B will insert "pdb.set_trace()" '
        event.cli.current_buffer.insert_text('\nimport pdb; pdb.set_trace()\n')

    # Custom key binding for some simple autocorrection while typing.

    corrections = {
        'impotr': 'import',
        'pritn': 'print',
        'pr': 'print(',
    }

    @repl.add_key_binding(' ')
    def _(event):
        ' When a space is pressed. Check & correct word before cursor. '
        b = event.cli.current_buffer
        w = b.document.get_word_before_cursor()
        if w is not None:
            if w in corrections:
                b.delete_before_cursor(count=len(w))
                b.insert_text(corrections[w])
        b.insert_text(' ')

    @repl.add_key_binding('?', filter=~IsInsideString(repl))
    def _docevent(event):
        j = KosmosShellConfig.j
        b = event.cli.current_buffer
        tbc = b.document.current_line_before_cursor.rstrip("(")
        d = get_doc_string(tbc)
        if d:
            repl.docstring_buffer.reset(document=Document(d, cursor_position=0))
        else:
            repl.docstring_buffer.reset()

    class CustomPrompt(PromptStyle):
        """
        The classic Python prompt.
        """

        def in_prompt(self):
            return [('class:prompt', 'JSX> ')]

        def in2_prompt(self, width):
            return [('class:prompt.dots', '...')]

        def out_prompt(self):
            return []

    repl.all_prompt_styles['custom'] = CustomPrompt()
    repl.prompt_style = 'custom'

    old_get_completions = repl._completer.__class__.get_completions

    def custom_get_completions(self, document, complete_event):
        try:
            _, _, prefix = get_current_line(document)
        except ValueError:
            return

        completions = list(old_get_completions(self, document, complete_event))
        if not completions:
            completions = get_completions(self, document, complete_event)
        yield from filter_completions_on_prefix(completions, prefix)

    repl._completer.__class__.get_completions = custom_get_completions

    setup_docstring_containers(repl)
