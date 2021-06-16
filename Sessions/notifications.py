from fcm_django.fcm import fcm_send_topic_message
from .models import Session

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
        + module_name + "\""
        +".\nStart time : " + start_time
        +"\nEnd time : " + end_time),
        message_title="New session created by teacher "+ teacher_name +".",
        message_icon="app_logo")

def notifySessionUpdated(oldSession, newSession):
    """
    Sends a push notification to the section about the update of the given session.
    """
    #Figure out which fields were modified and add them to a string.
    modified_fields = ""
    if oldSession.assignment.module_section.module.code != newSession.assignment.module_section.module.code:
        modified_fields += "Module : " + newSession.assignment.module_section.module.name + "\n"
    if oldSession.day != newSession.day:
        modified_fields += "Day : " + dict(Session.DaysOfWeek.choices)[newSession.day] + "\n"
    if oldSession.start_time != newSession.start_time:
        modified_fields += "Start time : " + str(newSession.start_time) + "\n"
    if oldSession.end_time != newSession.end_time:
        modified_fields += "End time : " + str(newSession.end_time) + "\n"
    if oldSession.concerned_groups != newSession.concerned_groups:
        modified_fields += "Concerned groups : " + str(newSession.concerned_groups) + "\n"
    if oldSession.meeting_link != newSession.meeting_link:
        modified_fields += "Meeting link : " + newSession.meeting_link + "\n"
    if oldSession.meeting_number != newSession.meeting_number:
        modified_fields += "Meeting number : " + newSession.meeting_number + "\n"
    if oldSession.meeting_password != newSession.meeting_password:
        modified_fields += "Meeting password : " + newSession.meeting_password + "\n"
    if oldSession.comment != newSession.comment:
        modified_fields += "Comment : " + newSession.comment + "\n"
    
    #Send the notification using the constructed string.
    section_code = newSession.assignment.teacher_section.section.code
    teacher_name = newSession.assignment.teacher_section.teacher.user.last_name
    old_module = oldSession.assignment.module_section.module.name
    fcm_send_topic_message(
        topic_name=section_code.replace(' ','_'),
        message_body=("Teacher "+ teacher_name + " updated a session for the module "+ old_module + ".\nModified information:\n"
        + modified_fields),
        message_title="Session updated by teacher "+ teacher_name +".",
        message_icon="app_logo")

def notifySessionDeleted(session):
    """
    Sends a push notification to the section about the deletion of the given session.
    """
    section_code = session.assignment.teacher_section.section.code
    teacher_name = session.assignment.teacher_section.teacher.user.last_name
    module_name = session.assignment.module_section.module.name
    fcm_send_topic_message(
        topic_name=section_code.replace(' ','_'),
        message_body=("Teacher "+ teacher_name + " removed a session for the module \""
        + module_name+ "\""),
        message_title="Session removed by teacher "+ teacher_name +".",
        message_icon="app_logo")
