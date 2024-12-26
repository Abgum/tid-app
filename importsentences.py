import aiohttp
import asyncio
import json


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Failed to fetch {url}: {response.status}")
            return None


async def post(session, url, data):
    async with session.post(url, json=data) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Failed to post to {url}: {response.status}")
            return None


async def main():
    async with aiohttp.ClientSession() as session:
        with open("Acil.json", "r", encoding="utf-8") as fp:
            acil_json = json.load(fp)

        book_id = 1
        for i, (sentence, files) in enumerate(acil_json.items(), start=1):
            sentence_data = {
                "nth_sentence": str(i),
                "book_id": str(book_id),
                "sentence": sentence,
                "transcript": ",".join(files)
            }
            print(sentence_data)
            created_sentence = await post(
                session,
                "http://127.0.0.1:2020/api/book_contents/add_sentence",
                sentence_data
            )
            print(created_sentence)
            if created_sentence is None:
                continue

            sentence_id = created_sentence["id"]
            print(sentence_id)
            for j, file in enumerate(files):
                url = "http://127.0.0.1:2020/api/transcripts/get_by_transcript_string/" + \
                    file.split(".")[0]
                print(f"Fetching {url}")
                response = await fetch(session, url)
                if response is None:
                    continue

                transcript_id = response["id"]
                print(transcript_id)
                st_data = {
                    "nth_transcription": j + 1,
                    "sentence_id": sentence_id,
                    "transcript_id": transcript_id,
                }
                await post(
                    session,
                    "http://127.0.0.1:2020/api/book_contents/add_sentence_transcription",
                    st_data
                )

asyncio.run(main())
