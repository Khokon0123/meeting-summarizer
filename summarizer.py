from transformers import pipeline

print("Loading BART summarization model...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
print("Model loaded!")

def chunk_text(text, max_chars=1000):
    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def summarize_text(text):
    if len(text) < 100:
        return "Text too short to summarize."
    chunks = chunk_text(text)
    print(f"Split into {len(chunks)} chunks...")
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1} of {len(chunks)}...")
        if len(chunk) > 50:
            summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
            chunk_summaries.append(summary[0]["summary_text"])
    return " ".join(chunk_summaries)

def extract_action_items(text):
    action_keywords = ["will ", "should ", "must ", "needs to", "action:", "todo:", "follow up", "by ", "deadline"]
    lines = text.lower().split('\n')
    action_items = []
    for line in lines:
        if any(keyword in line for keyword in action_keywords):
            if len(line.strip()) > 20:
                action_items.append(line.strip().capitalize())
    return action_items[:10]

def extract_attendees(text):
    lines = text.split('\n')
    for line in lines:
        if 'attendee' in line.lower() or 'present:' in line.lower():
            names = line.split(':', 1)[-1]
            return [n.strip() for n in names.split(',')]
    return []
