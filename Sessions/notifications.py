from fcm_django.fcm import fcm_send_topic_message

def notifySessionCreated(session):
    """
    Sends a push notification to the section about the creation of the given session.
    """
    section_code = session.assignment.teacher_section.section.code
    teacher_name = session.assignment.teacher_section.teacher.user.last_name
    module_name = session.assignment.module_section.module.name
    start_time = str(session.start_time)
    end_time = str(session.end_time)
    fcm_send_topic_message(
        topic_name=section_code.replace(' ','_'),
        message_body=("Teacher "+ teacher_name + " created a new session for the module \""
        + module_name
        +".\nStart time : " + start_time
        +"\nEnd time : " + end_time),
        message_title="New session created by teacher "+ teacher_name +".")

def notifySessionUpdated(session):
    """
    Sends a push notification to the section about the update of the given session.
    """
    section_code = session.assignment.teacher_section.section.code
    teacher_name = session.assignment.teacher_section.teacher.user.last_name
    module_name = session.assignment.module_section.module.name
    fcm_send_topic_message(
        topic_name=section_code.replace(' ','_'),
        message_body=("Teacher "+ teacher_name + " updated a session for the module \""
        + module_name),
        message_title="Session updated by teacher "+ teacher_name +".")

def notifySessionDeleted(session):
    """
    Sends a push notification to the section about the deletion of the given session.
    """
    section_code = session.assignment.teacher_section.section.code
    teacher_name = session.assignment.teacher_section.teacher.user.last_name
    module_name = session.assignment.module_section.module.name
    fcm_send_topic_message(
        topic_name=section_code.replace(' ','_'),
        message_body=("Teacher "+ teacher_name + " deleted a session for the module \""
        + module_name),
        message_title="Session deleted by teacher "+ teacher_name +".")
