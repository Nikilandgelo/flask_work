from flask import Response, jsonify, g, request
from sqlmodel import select
from serializers import AdvertisementSerializer
from models import Advertisement
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


def adverts_list():
    adverts = g.session.execute(
        select(Advertisement)
    ).scalars().all()

    validated_adverts = [AdvertisementSerializer.model_validate(advert).model_dump()
                         for advert in adverts]
    return jsonify(validated_adverts), 200

def adverts_post() -> Response:
    try:
        validated_advert = AdvertisementSerializer(**request.json).model_dump()
    except ValidationError as error:
        errors = error.errors(include_url=False, include_input=False, include_context=False)
        return jsonify(errors), 400
    
    advert = Advertisement(**validated_advert)
    g.session.add(advert)
    
    try:
        g.session.commit()
    except IntegrityError as error:
        return Response(error.orig.args)
    
    return Response("Advert has been created", 201)

def adverts_retrieve(pk):
    advert = _find_advert(pk)
    if advert:
        return jsonify(AdvertisementSerializer.model_validate(advert).model_dump()), 200
    else:
        return _advert_not_found()

def adverts_patch(pk):
    advert = _find_advert(pk)
    if advert:
        if advert.owner_id != request.json.get("owner_id"):
            return Response("Change adverts only possible for creator", 400)
        
        for key, value in request.json.items():
            try:
                setattr(advert, key, value)
            except ValueError as error:
                return Response(str(error), 404)
        
        try:
            AdvertisementSerializer.model_validate(advert)
        except ValidationError as error:
            errors = error.errors(include_url=False, include_input=False, include_context=False)
            return jsonify(errors), 400
        
        g.session.add(advert)
        g.session.commit()
        return Response("Advert has been updated"), 200
    else:
        return _advert_not_found()

def adverts_delete(pk):
    advert = _find_advert(pk)
    if advert:
        g.session.delete(advert)
        g.session.commit()
        return Response('Adverts has been deleted', 200)
    else:
        return _advert_not_found()


def _find_advert(pk) -> Advertisement | None:
    advert: Advertisement = g.session.execute(
        select(Advertisement)
        .where(Advertisement.id == pk)
    ).scalar()
    return advert

def _advert_not_found() -> Response:
    return Response('Advert with that id not exists', 404)