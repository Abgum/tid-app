from data_access import (
    sentences,
    sentence_transcriptions,
    user_book_histories,
    transcripts,
)


def get_book_contents(book_id):
    sentence_list = sentences.get_sentences_by_book_id(book_id)
    for sentence in sentence_list:
        transcriptions = (
            sentence_transcriptions.get_sentence_transcription_by_sentence_id(
                sentence["id"]
            )
        )
        sentence["transcriptions"] = [
            transcripts.get_transcript_by_id(transcription["transcript_id"])
            for transcription in transcriptions
        ]
    return sentence_list, 200


def add_sentence(sentence_payload):
    nth_sentence = sentence_payload["nth_sentence"]
    book_id = sentence_payload["book_id"]
    sentence = sentence_payload["sentence"]
    return sentences.create_sentence(nth_sentence, sentence, book_id), 200


def add_sentence_transcription(st_payload):
    transcript_id = st_payload["transcript_id"]
    sentence_id = st_payload["sentence_id"]
    nth_transcription = st_payload["nth_transcription"]
    return sentence_transcriptions.create_sentence_transcription(
        sentence_id, transcript_id, nth_transcription
    ), 200


def add_transcription(transcript_payload):
    media_path = transcript_payload["media_path"]
    transcription = transcript_payload["transcription"]
    return transcripts.create_transcript(media_path, transcription), 200


def get_last_read_sentence(last_read_sentence_payload):
    book_id = last_read_sentence_payload["book_id"]
    user_id = last_read_sentence_payload["user_id"]
    return user_book_histories.get_user_book_history(user_id, book_id), 200


def update_last_read_sentence(last_read_sentence_update_payload):
    book_id = last_read_sentence_update_payload["book_id"]
    user_id = last_read_sentence_update_payload["user_id"]
    last_sentence_id = last_read_sentence_update_payload["last_sentence_id"]
    return user_book_histories.update_user_book_history(
        user_id, book_id, last_sentence_id
    ), 200
