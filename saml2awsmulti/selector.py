from PyInquirer import prompt, style_from_dict, Token


custom_style = style_from_dict({
    Token.Separator: "#6C6C6C",
    Token.QuestionMark: "#FF9D00 bold",
    Token.Selected: "#5F819D",
    Token.Pointer: "#FF9D00 bold",
    Token.Instruction: "",  # default
    Token.Answer: "#5F819D bold",
    Token.Question: "",
})


def prompt_profile_selection(options):
    questions = [{
        "choices": options,
        "message": "Please choose the profile",
        "name": "profile",
        "type": "list",
    }]
    return prompt(questions, style=custom_style)


def prompt_roles_selection(options, last_selected_options):
    questions = [{
        "choices": [dict({
            "name": role,
            "checked": True if role in last_selected_options else False}
        ) for role in options],
        "message": "Please choose the role",
        "name": "roles",
        "type": "checkbox",
    }]
    return prompt(questions, last_selected_options, style=custom_style)
