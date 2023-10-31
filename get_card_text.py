# create card 
'''
'name'
'profession'
'hobby'
'situation'
'difficulties'
'communication'
'additional'

Example use: 
create_card(name="Jack", profession="driver", hobby="go for walks",  difficulties="hear")

'''
def create_card(**kwargs):
    if not kwargs:
        return "Please provide more information about yourself to create a card."
    name = f'I’m {kwargs["name"]}.' if 'name' in kwargs else ""
    profession = f"I am/was a {kwargs['profession']}." if 'profession' in kwargs else ""
    hobby = f'I like to {kwargs["hobby"]}.' if "hobby" in kwargs else ''
    situation = ''
    difficulties = ''
    if 'situation' in kwargs and 'difficulties' in kwargs:
        situation = f'I {kwargs["situation"]} and it\'s hard for me to ' 
        difficulties = f'{kwargs["difficulties"]}.'
    elif 'situation' in kwargs:
        situation = f'I {kwargs["situation"]}.'
    elif 'difficulties' in kwargs:
        difficulties = f'It\'s now hard for me to {kwargs["difficulties"]}.'
    
    communication = f'Please help me by {kwargs["communication"]}.' if "communication" in kwargs else ''
    additional = f'\n {kwargs["additional"]}' if 'additional' in kwargs else ''
    s = f"""Hi!
{name}{profession}{hobby} 
{situation}{difficulties}
{communication} 
Thank you! {additional}"""

    return s