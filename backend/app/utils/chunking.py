import re


def split_into_semantic_chunks(
	text: str,
	chunk_size: int,
	overlap: int,
) -> list[str]:
	paragraphs = [paragraph.strip() for paragraph in re.split(r"\n{2,}", text) if paragraph.strip()]
	chunks: list[str] = []
	current_sentences: list[str] = []
	current_length = 0

	for paragraph in paragraphs:
		sentences = re.split(r"(?<=[.!?])\s+", paragraph)
		for sentence in sentences:
			sentence = sentence.strip()
			if not sentence:
				continue

			prospective_length = current_length + len(sentence) + (1 if current_sentences else 0)
			if current_sentences and prospective_length > chunk_size:
				chunk = " ".join(current_sentences).strip()
				chunks.append(chunk)
				current_sentences = _build_overlap_sentences(chunk, overlap)
				current_length = len(" ".join(current_sentences))

			current_sentences.append(sentence)
			current_length = len(" ".join(current_sentences))

	if current_sentences:
		chunks.append(" ".join(current_sentences).strip())

	return [chunk for chunk in chunks if chunk]


def _build_overlap_sentences(chunk: str, overlap: int) -> list[str]:
	if overlap <= 0:
		return []

	sentences = re.split(r"(?<=[.!?])\s+", chunk)
	selected: list[str] = []
	current_length = 0
	for sentence in reversed(sentences):
		if not sentence:
			continue
		selected.insert(0, sentence)
		current_length += len(sentence)
		if current_length >= overlap:
			break
	return selected