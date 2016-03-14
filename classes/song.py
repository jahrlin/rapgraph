import graphene

class Song(graphene.ObjectType):
    artist = graphene.String(description = 'Primary artist name')
        
