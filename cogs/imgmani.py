from discord.ext import commands
import discord
import typing
from PIL import Image, ImageDraw,ImageChops,ImageOps,ImageFont,ImageFilter
from io import BytesIO
from typing import Optional



def crop_to_circle(im):
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, im.split()[-1])
    im.putalpha(mask)
    return im



filters = {
   
"blur": ImageFilter.BLUR,
"contour": ImageFilter.CONTOUR,
"detail": ImageFilter.DETAIL,
"edgeenhance": ImageFilter.EDGE_ENHANCE,
"edgeenhancemore":ImageFilter.EDGE_ENHANCE_MORE,
"emboss": ImageFilter.EMBOSS,
"findedges": ImageFilter.FIND_EDGES,
"sharpen": ImageFilter.SHARPEN,
"smooth":ImageFilter.SMOOTH,
"smoothmore": ImageFilter.SMOOTH_MORE,
"boxblur": ImageFilter.BoxBlur(1),
"gaussianblur": ImageFilter.GaussianBlur(5),
"unsharpmax": ImageFilter.UnsharpMask
}


class img(commands.Cog):

  def __innit__(self,client):
    self.client = client

  
  @commands.command()
  @commands.cooldown(1,5,commands.BucketType.user)
  async def wanted(self,ctx,user: discord.Member = None):
    user = user or ctx.author

    with Image.open("./images/wanted.png") as wanted:

      wanted = wanted.convert("RGBA")
      asset = user.avatar_url_as(size = 128)

      data = BytesIO(await asset.read())

      pfp = Image.open(data)
      
      pfp = pfp.resize((220,216))

      wanted.paste(pfp, (83,163))
      wanted.save("./images/profile.png")
    await ctx.send(file = discord.File("./images/profile.png"))

  @commands.command()
  @commands.cooldown(1,5,commands.BucketType.user)
  async def filter(self,ctx,mode="emboss",user: discord.Member = None):
    user = user or ctx.author

    asset = user.avatar_url#_as(size = 128)

    data = BytesIO(await asset.read())
    img=Image.open(data).convert("RGBA")
    
    
    img = img.filter(filters[mode])
    #asset = asset.resize((220,216))

    

    img.save("./images/white.png")
    await ctx.send(file = discord.File("./images/white.png"))

  @commands.command()
  async def quote(self,ctx,user: Optional[discord.Member],*,text:str):    
    user = user or ctx.author
    if not text:
      await ctx.send("quote what?")
    
    with Image.open("./images/quote.png") as quote:
      quote = quote.convert("RGBA")
      asset = user.avatar_url
      font=ImageFont.truetype("./fonts/Fira Sans Regular 400.ttf",16)
      font1=ImageFont.truetype("./fonts/arial.ttf",10)
      font2=ImageFont.truetype("./fonts/arial.ttf",14)
      #font1=ImageFont.truetype("Uni Sans Thin.otf",6)
      
      data = BytesIO(await asset.read())
      img=Image.open(data).convert("RGBA")
      circ_pfp = crop_to_circle(img)
      
      circ_pfp = circ_pfp.resize((44,44))    
      #circ_pfp = circ_pfp.filter(filters["edge enhance more"])
      quote.paste(circ_pfp, (5,27))

      user_name = (71,29)
     
      draw = ImageDraw.Draw(quote)
      draw.text((user_name),text="".join({user.name}),font=font)
      draw.text((user_name[0]+font.getsize(str(user.name))[0]+7,34),text="".join("Today at " + ctx.message.created_at.strftime("%H:%M")),fill = (128,128,128),font = font1)
      draw.text((71,55),text="".join(text),font=font2,fill=(192,192,192))
      
      quote.save("./images/quoted.png")
    await ctx.send(file = discord.File("./images/quoted.png"))
  

  @commands.command()
  async def icard(self,ctx,user: Optional[discord.Member]):#,pos:str,rat:int):    
    user = user or ctx.author
    
    
    with Image.open("./images/iconic.png") as iconic:
      iconic = iconic.convert("RGBA")
      asset = user.avatar_url_as(size = 128)
      data = BytesIO(await asset.read())
      font=ImageFont.truetype("./fonts/Fira Sans Regular 400.ttf",16)
      img=Image.open(data).convert("RGBA")
      img = img.resize((136,136))
      draw = ImageDraw.Draw(iconic)
      draw.text((29,202),text = f"{user.name}",font = font)
      iconic.paste(img,(29,59))
      iconic.save("./images/icard.png")
    await ctx.send(file=discord.File("./images/icard.png"))
 
 
  
def setup(client):
    client.add_cog(img(client))



