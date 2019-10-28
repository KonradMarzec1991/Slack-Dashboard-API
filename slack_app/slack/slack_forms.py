"""
Slack resource with forms to display
"""

import json


def create_ticket_form(text=""):
    dialog = {
        "callback_id": "ryde-46e2b0",
        "title": "Create todo",
        "submit_label": "Submit",
        "notify_on_cancel": True,
        "state": "Limo",
        "elements": [
            {
                "label": "Title",
                "type": "text",
                "name": "title",
                "placeholder": "my_ticket...",
                "value": text
            },
            {
                "label": "Description",
                "type": "textarea",
                "name": "description",
                "hint": "Write details of ticket"
            },
            {
                "label": "Meal preferences",
                "type": "select",
                "name": "meal_preferences",
                "options": [
                    {
                        "label": "Hindu (Indian) vegetarian",
                        "value": "hindu"
                    },
                    {
                        "label": "Strict vegan",
                        "value": "vegan"
                    },
                    {
                        "label": "Kosher",
                        "value": "kosher"
                    },
                    {
                        "label": "Just put it in a burrito",
                        "value": "burrito"
                    }
                ]
            },
            {
                "label": "Meal preferences",
                "type": "select",
                "name": "meal_preferences",
                "options": [
                    {
                        "label": "Hindu (Indian) vegetarian",
                        "value": "hindu"
                    },
                    {
                        "label": "Strict vegan",
                        "value": "vegan"
                    },
                    {
                        "label": "Kosher",
                        "value": "kosher"
                    },
                    {
                        "label": "Just put it in a burrito",
                        "value": "burrito"
                    }
                ]
            }
        ]
    }

    return json.dumps(dialog)
