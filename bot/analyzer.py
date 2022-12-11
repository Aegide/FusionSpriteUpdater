from discord import Embed, Message
import discord
from bot.enums import Severity
from bot.issues import Issue
from bot.enums import DiscordColour
import bot.utils as utils
import bot.analysis_content as analysis_content
import bot.analysis_sprite as analysis_sprite


DICT_SEVERITY_COLOUR = {
    Severity.accepted : DiscordColour.green,
    Severity.ignored : DiscordColour.orange,
    Severity.refused : DiscordColour.red
}


class Analysis:
    message: Message
    issues: list[Issue] = []
    severity: Severity = Severity.accepted
    embed: Embed
    autogen_url: str|None = None
    attachment_url: str|None = None
    fusion_id = str

    def __init__(self, message:Message) -> None:
        self.message = message

    def generate_embed(self):
        self.embed = discord.Embed()
        self.apply_title()
        self.apply_colour()
        self.apply_author()
        self.apply_footer()
        self.apply_autogen_url()
        self.apply_attachment_url()

    def apply_title(self):
        if self.severity == Severity.accepted:
            self.embed.title = f"__{Severity.accepted.value} : {self.fusion_id}__"
        else:
            self.embed.title = f"__{Severity.ignored.value} : (ISSUES)__"

    def apply_colour(self):
        self.embed.colour = DICT_SEVERITY_COLOUR.get(self.severity, DiscordColour.gray).value

    def apply_description(self):
        self.embed.description = f"[Link to message]({self.message.jump_url})"

    def apply_author(self):
        author_avatar = utils.get_display_avatar(self.message.author)
        self.embed.set_author(name=self.message.author.name, icon_url=author_avatar.url)

    def apply_footer(self):
        self.embed.set_footer(text=self.message.content)

    def apply_autogen_url(self):
        if self.autogen_url is not None:
            self.embed.set_image(url=self.autogen_url)

    def apply_attachment_url(self):
        if self.attachment_url is not None:
            self.embed.set_thumbnail(url=self.attachment_url)


def generate_analysis(message:Message):
    analysis = Analysis(message)
    analysis_content.main(analysis)
    analysis_sprite.main(analysis)
    analysis.generate_embed()
    return analysis

