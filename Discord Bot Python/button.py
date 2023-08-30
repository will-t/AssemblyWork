#This file is for the SimpleView class that contains the buttons
import discord
import commands

class SimpleView(discord.ui.View):
    
    #var : bool = None

    #async def disable_buttons(self):
    #    for item in self.children:
    #        item.disabled = True
    #        await self.message.edit(view=self)

    #async def on_timeout(self):
    #    await self.message.channel.send("Timed out")
    #    await self.disable_buttons()

    @discord.ui.button(label='Play', style=discord.ButtonStyle.green)
    async def play1(self, interaction: discord.Interaction, button: discord.ui.Button):
            await resume(self.message)



        #self.var = True
        

    @discord.ui.button(label='Pause', style=discord.ButtonStyle.blurple)
    async def pause1(self, interaction: discord.Interaction, button: discord.ui.Button):
            await pause(self.message)
        #self.var = True
        
        

    @discord.ui.button(label='Stop', style=discord.ButtonStyle.red)
    async def stop1(self, interaction: discord.Interaction, button: discord.ui.Button):
            await stop(self.message)

        #self.var = False

    @discord.ui.button(label='Skip', style=discord.ButtonStyle.grey)
    async def skip1(self, interaction: discord.Interaction, button: discord.ui.Button):
            await skip_song(self.message)
        #self.var = False
        


async def button_function(message):

    view = SimpleView(timeout=300)
    
    message = await message.channel.send(view=view)
    view.message = message
    await view.wait()
    #await view.disable_buttons()
    
    #if view.var is None:
    #    print("Timeout")

    #elif view.var is True:
    #    print("OK")

    #elif view.var is False:
    #    print("Cancel")