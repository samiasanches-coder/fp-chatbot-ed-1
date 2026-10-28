from app.chatbot import Chatbot


def test_chatbot_response_includes_user_input():
    bot = Chatbot()
    response = bot.respond("hello")
    assert isinstance(response, str)
    assert len(response) > 0


def test_input_guard_rejects_empty_message():
    from safety.input_guard import InputGuard

    result = InputGuard().validate("")
    assert result["safe"] is False
