import datetime


def export_chat(messages):
    """
    Convert chat history into a downloadable text format.
    """

    if not messages:
        return "No chat available."

    output = []

    output.append("=" * 60)
    output.append("SMART PDF INSIGHT ASSISTANT")
    output.append("=" * 60)
    output.append("")

    output.append(
        f"Generated on: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

    output.append("")
    output.append("=" * 60)
    output.append("CHAT HISTORY")
    output.append("=" * 60)
    output.append("")

    for i, chat in enumerate(messages, start=1):

        output.append(f"Question {i}")
        output.append(chat["question"])
        output.append("")

        output.append(f"Answer {i}")
        output.append(chat["answer"])
        output.append("")

        output.append("-" * 60)
        output.append("")

    return "\n".join(output)