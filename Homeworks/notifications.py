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
        data_message={"test_data":"test data"})

def notifyHomeworkUpdated(homework):
    """
    Sends a push notification to the section about the update of the given homework.
    """
    section_code = homework.assignment.teacher_section.section.code
    teacher_name = homework.assignment.teacher_section.teacher.user.last_name
    module_name = homework.assignment.module_section.module.name
    fcm_send_topic_message(
        topic_name=section_code.replace(' ','_'),
        message_body=("Teacher "+ teacher_name + " updated a homework for the module \""
        + module_name + "\""),
        message_title="A homework has been updated by teacher "+ teacher_name +".")

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
        message_title="A homework has been removed by teacher "+ teacher_name +".")
