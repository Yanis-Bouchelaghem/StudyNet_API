from fcm_django.fcm import fcm_send_topic_message

def notifyHomeworkCreated(homework):
    """
    Sends a push notification to the section about the creation of the given homework.
    """
    section_code = homework.assignment.teacher_section.section.code
    teacher_name = homework.assignment.teacher_section.teacher.user.last_name
    module_name = homework.assignment.module_section.module.name
    fcm_send_topic_message(
        topic_name=section_code.replace(' ','_'),
        message_body=("Teacher "+ teacher_name + " created a new homework for the module \""
        + module_name +"\""),
        message_title="New homework created by teacher "+ teacher_name +".",
        data_message={"test_data":"test data"},
        message_icon="app_logo")

def notifyHomeworkUpdated(oldHomework, newHomework):
    """
    Sends a push notification to the section about the update of the given homework.
    """
    #Figure out which fields were modified and add them to a string.
    modified_fields = ""
    if oldHomework.assignment.module_section.module.code != newHomework.assignment.module_section.module.code:
        modified_fields += "Module : " + newHomework.assignment.module_section.module.name + "\n"
    if oldHomework.concerned_groups != newHomework.concerned_groups:
        modified_fields += "Concerned groups : " + str(newHomework.concerned_groups) + "\n"
    if oldHomework.title != newHomework.title:
        modified_fields += "Title : " + newHomework.title + "\n"
    if oldHomework.due_date != newHomework.due_date:
        modified_fields += "Due date : " + str(newHomework.due_date) + "\n"
    if oldHomework.due_time != newHomework.due_time:
        modified_fields += "Due time : " + str(newHomework.due_time) + "\n"
    if oldHomework.comment != newHomework.comment:
        modified_fields += "Comment : " + newHomework.comment + "\n"

    #Send the notification using the constructed string.
    section_code = newHomework.assignment.teacher_section.section.code
    teacher_name = newHomework.assignment.teacher_section.teacher.user.last_name
    old_module = oldHomework.assignment.module_section.module.name
    fcm_send_topic_message(
        topic_name=section_code.replace(' ','_'),
        message_body=("Teacher "+ teacher_name + " updated a homework for the module "+ old_module + ".\nModified information:\n"
        + modified_fields),
        message_title="A homework has been updated by teacher "+ teacher_name +".",
        message_icon="app_logo")

def notifyHomeworkDeleted(session):
    """
    Sends a push notification to the section about the deletion of the given homework.
    """
    section_code = session.assignment.teacher_section.section.code
    teacher_name = session.assignment.teacher_section.teacher.user.last_name
    module_name = session.assignment.module_section.module.name
    fcm_send_topic_message(
        topic_name=section_code.replace(' ','_'),
        message_body=("Teacher "+ teacher_name + " removed a homework for the module \""
        + module_name + "\""),
        message_title="A homework has been removed by teacher "+ teacher_name +".",
        message_icon="app_logo")
