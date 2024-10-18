from rest_framework.decorators import api_view
from rest_framework.response import Response
from studyroom.models import Room
from .serializer import RoomSerializer

@api_view(['GET'])
def routeView(requests):
    routes = [
        'GET /api/',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    print(serializer)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request,pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    print(serializer)
    return Response(serializer.data)