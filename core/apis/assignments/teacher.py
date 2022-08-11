from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
import json


from .schema import AssignmentSchema, AssignmentGradeSchema

teacher_resource = Blueprint('teacher_resource', __name__)



@teacher_resource.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments_teacher(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)

@teacher_resource.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def upsert_assignments(p, incoming_payload):
    """Create or Edit an assignment"""
    
    assignment = AssignmentGradeSchema().load(incoming_payload)
    assignment.teacher_id = p.teacher_id
    upserted_assignment = Assignment.upserts(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)
