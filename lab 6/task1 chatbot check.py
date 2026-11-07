from guided_chatbot import build_bot, reply
engine = build_bot()
assert "it_help.txt" in reply(engine, "How do I reset my password?")
assert "it_help.txt" in reply(engine, "how do i connect to the campus wi-fi?")
assert "fee_rules.txt" in reply(engine, "How do I pay my semester fee?")
assert reply(engine, "") == "Please enter a question."
assert "No matching FAQ" in reply(engine, "volcano geology")
assert "Possible matches" in reply(engine, "password recovery")
print("FAQ behaviour checks passed")
