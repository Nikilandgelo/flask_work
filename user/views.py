from flask import Response, jsonify, g, request
from sqlmodel import select
from models import User
from serializers import UserSerializer, UserCreateUpdateSerializer
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


def user_list() -> Response:
    users = g.session.execute(
        select(User)
    ).scalars().all()
    
    validated_users = [UserSerializer.model_validate(user).model_dump() for user in users]
    return jsonify(validated_users), 200

def user_post() -> Response:
    try:
        validated_user = UserCreateUpdateSerializer(**request.json).model_dump()
    except ValidationError as error:
        errors = error.errors(include_url=False, include_input=False, include_context=False)
        return jsonify(errors), 400
    
    user = User(**validated_user)
    g.session.add(user)
    
    try: 
        g.session.commit()
    except IntegrityError as error:
        return Response(error.orig.args)

    return Response('User has been created', 201)
        
def user_retrieve(pk) -> Response:
    user = _find_user(pk)
    if user:
        return jsonify(UserSerializer.model_validate(user).model_dump()), 200
    else:
        return _user_not_found()

def user_delete(pk) -> Response:
    user = _find_user(pk)
    if user:
        g.session.delete(user)
        g.session.commit()
        return Response('User has been deleted', 200)
    else:
        return _user_not_found()


def _find_user(pk):
    user = g.session.execute(
        select(User)
        .where(User.id == pk)
    ).scalar()
    return user

def _user_not_found() -> Response:
    return Response('User with that id not exists', 404)