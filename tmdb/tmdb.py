from html import escape

from mautrix.types import TextMessageEventContent, MediaMessageEventContent, MessageType, Format, RelatesTo, RelationType

from maubot import Plugin, MessageEvent
from maubot.handlers import command

from tmdb.tmdb_api import Movie

class TmdbBot(Plugin):

    async def send_movie_info(self, evt: MessageEvent, movie) -> None:
        mxc_uri = await self.client.upload_media(data=movie.get_image_binary())
        text_message = f'{movie.title}'
        if len(movie.overview) > 200:
            three_dotts = " [...]"
        else:
            three_dotts = ""
        html_message = f"""<p><b>{escape(movie.title)}</b></p>
        <p>{escape(movie.overview)[:200]}{three_dotts}</p>
        <p>taken from www.themoviedb.org</p>"""
        content = TextMessageEventContent(
            msgtype=MessageType.TEXT, format=Format.HTML,
            body=f"{text_message}",
            formatted_body=f"{html_message}")
        await evt.respond(content)
        content = MediaMessageEventContent(
            msgtype=MessageType.IMAGE,
            body=f"Image {movie.title}",
            url=f"{mxc_uri}")
        await evt.respond(content)


    @command.new("movie-id", help="Movie lookup by id")
    @command.argument("message", pass_raw=True, required=True)
    async def movie_id(self, evt: MessageEvent, message: str = "") -> None:
        movie = Movie()
        movie.query_details(message)
        await self.send_movie_info(evt, movie)


    @command.new("movie-search", help="Movie lookup by Title")
    @command.argument("message", pass_raw=True, required=True)
    async def movie_search(self, evt: MessageEvent, message: str = "") -> None:
        movie = Movie()
        movie.search_title(message)
        if movie.valid:
            await self.send_movie_info(evt, movie)
        else:
            content = TextMessageEventContent(
            msgtype=MessageType.NOTICE, format=Format.HTML,
            body=f"No movie found!")
        await evt.respond(content)
