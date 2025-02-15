skills = {
    "коммуникабельность": 0,
    "интеллект": 0,
    "физическая сила": 0,
    "харизма": 0,
    "удача": 0
}

required_skills_for_chapter_2 = 10

def upgrade_skill(skill):
    if skill in skills:
        skills[skill] += 1
        print(f"Вы улучшили навык '{skill}' до уровня {skills[skill]}.")

def check_skills_for_chapter_2(gender, name, new_friend_name, location):
    if sum(skills.values()) >= required_skills_for_chapter_2:
        chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skills.values())} навыков, чтобы перейти к следующей главе.")
