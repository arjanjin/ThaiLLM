"""Interactive CLI chatbot using the ThaiLLM Pathumma API."""

from thaillm_client import chat


def main():
    print("ThaiLLM Pathumma Chatbot (พิมพ์ 'exit' เพื่อออก)")
    print("-" * 50)

    messages = []

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nลาก่อน!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "ออก"):
            print("ลาก่อน!")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            data = chat(messages)
            reply = data["choices"][0]["message"]["content"]
            print(f"\nAssistant: {reply}")
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"\nError: {e}")
            messages.pop()  # remove failed user message


if __name__ == "__main__":
    main()
