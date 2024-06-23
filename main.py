from manon_chat_interface.modules.entity_recognition import entity_recognition

input = """
Can creality ender manufacture flange additive?
"""

response = entity_recognition(input=input)
print(response)
