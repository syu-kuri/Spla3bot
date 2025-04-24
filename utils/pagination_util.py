import io
from typing import Self, List, Optional, Tuple

import discord

from utils.image_util import ImageUtil


class PaginationView(discord.ui.View):
    def __init__(self: Self, match: str, embeds: List[discord.Embed], images: List[Tuple[str, str]], timeout: Optional[float] = 180.0):
        super().__init__(timeout=timeout)
        self.match = match
        self.embeds = embeds
        self.images = images
        self.current_page = 0
        self.total_page = len(embeds)
        self.update_buttons()

    def update_buttons(self: Self):
        self.first_page.disabled = self.current_page == 0
        self.prev_page.disabled = self.current_page == 0
        self.next_page.disabled = self.current_page == len(self.embeds) - 1
        self.last_page.disabled = self.current_page == len(self.embeds) - 1

    def gen_file(self: Self, embed: discord.Embed, image: List[Tuple[str, str]]) -> Tuple[discord.Embed, discord.File]:
        # generate stage image
        img = ImageUtil.gen_image_by_url(url1=image[0], url2=image[1])
        img_binary = io.BytesIO()
        img.save(img_binary, format='PNG')
        img_binary.seek(0)

        # discord File
        file = discord.File(img_binary, filename='image.png')

        embed.set_image(url="attachment://image.png")

        return embed, file

    @discord.ui.button(emoji="⏮️", style=discord.ButtonStyle.grey)
    async def first_page(self: Self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = 0
        self.update_buttons()

        embed = self.embeds[self.current_page]
        image = self.images[self.current_page]

        embed.set_footer(text="{}/{}".format(self.current_page + 1, self.total_page))

        if self.match in ['regular', 'bankara-challenge', 'bankara-open', 'x']:
            embed, file = self.gen_file(embed=embed, image=image)
            await interaction.message.edit(embed=embed, attachments=[file], view=self)
            await interaction.response.defer()
        elif self.match == 'coop':
            await interaction.message.edit(embed=embed, view=self)
            await interaction.response.defer()

    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.grey)
    async def prev_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.update_buttons()

        embed = self.embeds[self.current_page]
        image = self.images[self.current_page]

        embed.set_footer(text="{}/{}".format(self.current_page + 1, self.total_page))

        if self.match in ['regular', 'bankara-challenge', 'bankara-open', 'x']:
            embed, file = self.gen_file(embed=embed, image=image)
            await interaction.message.edit(embed=embed, attachments=[file], view=self)
            await interaction.response.defer()
        elif self.match == 'coop':
            await interaction.message.edit(embed=embed, view=self)
            await interaction.response.defer()

    @discord.ui.button(emoji="❌", style=discord.ButtonStyle.grey)
    async def stop_pages(self: Self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=None)

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.grey)
    async def next_page(self: Self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.update_buttons()

        embed = self.embeds[self.current_page]
        image = self.images[self.current_page]

        embed.set_footer(text="{}/{}".format(self.current_page + 1, self.total_page))

        if self.match in ['regular', 'bankara-challenge', 'bankara-open', 'x']:
            embed, file = self.gen_file(embed=embed, image=image)
            await interaction.message.edit(embed=embed, attachments=[file], view=self)
            await interaction.response.defer()
        elif self.match == 'coop':
            await interaction.message.edit(embed=embed, view=self)
            await interaction.response.defer()

    @discord.ui.button(emoji="⏭️", style=discord.ButtonStyle.grey)
    async def last_page(self: Self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = len(self.embeds) - 1
        self.update_buttons()

        embed = self.embeds[self.current_page]
        image = self.images[self.current_page]

        embed.set_footer(text="{}/{}".format(self.current_page + 1, self.total_page))

        if self.match in ['regular', 'bankara-challenge', 'bankara-open', 'x']:
            embed, file = self.gen_file(embed=embed, image=image)
            await interaction.message.edit(embed=embed, attachments=[file], view=self)
            await interaction.response.defer()
        elif self.match == 'coop':
            await interaction.message.edit(embed=embed, view=self)
            await interaction.response.defer()


class PaginationUtil:
    @staticmethod
    async def start(interaction: discord.Interaction, match: str, embeds: List[discord.Embed], images: List[str], timeout: Optional[float] = 180.0) -> None:
        """
        Pagination method.

        Arguments
        ---------
        interaction: discord.Interaction
        embeds: List[discord.Embed]
        images: List[Tuple[str, str]]
        timeout: Optional[float] Default=180.0
        """
        if not embeds:
            return

        if not images:
            return

        view = PaginationView(match, embeds, images, timeout)

        image = images[0]

        if match in ['regular', 'bankara-challenge', 'bankara-open', 'x']:
            # generate stage image
            img = ImageUtil.gen_image_by_url(url1=image[0], url2=image[1])
            img_binary = io.BytesIO()
            img.save(img_binary, format='PNG')
            img_binary.seek(0)

            # discord File
            file = discord.File(img_binary, filename='image.png')

            embed = embeds[0]
            embed.set_image(url="attachment://image.png")
            embed.set_footer(text="{}/{}".format(1, len(embeds)))

            await interaction.followup.send(embed=embed, file=file, view=view)
        elif match == 'coop':
            embed = embeds[0]
            embed.set_footer(text="{}/{}".format(1, len(embeds)))
            await interaction.followup.send(embed=embed, view=view)
