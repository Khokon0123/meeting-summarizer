# Meeting Notes Summarizer

Paste meeting notes or upload a text file and get a short summary, a list of action items, and the attendees. Built with a pretrained DistilBART summarization model and a Streamlit interface.

**Live demo:** _add your link here after deploying_

## What it does

- Accepts meeting notes by pasting text or uploading a `.txt` file
- Splits long notes into chunks so they fit the model's input limit, summarizes each chunk, and joins the results into one summary
- Pulls out likely action items (lines with phrases like "will", "must", "needs to", "by", "deadline")
- Detects attendees from an `Attendees:` line
- Lets you download the summary and action items as a text file

## How it works

```
Meeting notes -> split into ~1000-character chunks
              -> summarize each chunk (sshleifer/distilbart-cnn-6-6)
              -> combine into the final summary

Meeting notes -> keyword scan -> action items
              -> "Attendees:" line -> attendee list
```

## Tech stack

| Component | Tool |
|---|---|
| Summarization model | sshleifer/distilbart-cnn-6-6 (Hugging Face Transformers) |
| Runtime | PyTorch (CPU) |
| Interface | Streamlit |
| Hosting | Streamlit Community Cloud |

DistilBART is a smaller, faster version of BART. It was chosen so the app fits within the memory limits of free hosting.

## Project structure

```
meeting-summarizer/
├── app.py              # Streamlit interface
├── summarizer.py       # Chunking, summarization, action items, attendees
├── sample_meeting.txt  # Example notes to try
└── requirements.txt
```

## Run it locally

Requires Python 3.11. Newer Python versions may not yet be supported by the model libraries.

```bash
git clone https://github.com/Khokon0123/meeting-summarizer.git
cd meeting-summarizer
python3.11 -m venv env
source env/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The first run downloads the model. After that it loads from your local cache.

## Example input

```
Meeting: Robotics Club
Attendees: Alex, Jordan, Sam

We discussed the competition budget.
Alex will submit the budget by July 1st.
Jordan will order the sensors next week.
Next meeting is July 15th.
```

Notes work best when each decision or task is written as its own line, and when attendees are listed on a line starting with `Attendees:`.

## Privacy

On the hosted demo, text you paste is processed on a remote server. Do not paste confidential or sensitive notes into it. To keep notes private, run the app locally as shown above; nothing leaves your computer.

## Limitations

- Action items come from keyword matching, not understanding. Some real tasks will be missed and some non-tasks will be included.
- Action items are shown in lowercase because of how lines are processed.
- The summary is built chunk by chunk, so very long notes can lose connections between sections.
- The model is trained on news articles, so summaries of informal notes can be uneven.
- Only plain text input is supported.
- The hosted app goes to sleep after a period without visitors, so the first load can take a minute or two.

## Possible improvements

- Use an instruction-following language model to extract tasks with owners and deadlines
- Support PDF and audio transcript input
- Keep original capitalization in action items
- Export to Markdown or PDF

## Skills demonstrated

Working with pretrained transformer models, handling input length limits through chunking, basic text extraction, trading model size against hosting limits, and building and deploying a Streamlit application.
