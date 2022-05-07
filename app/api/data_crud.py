from flask import Flask
from flask import request
from flask import current_app as app
from app.redisclient import redis_client
import json
import logging
import redis   
rd3 = redis_client(3) # for generic data
rd4 = redis_client(4) # for musicpy objects



# place non-route functions outside of class




# name class same as filename
class data_crud():

    # CREATE/READ/UPDATE/DELETE methods all in this route
    @app.route('/songlist', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def routes(index):
        '''
        General function that holds all the methods of the /songlist route.
    
        FOR DEV PURPOSES, 'songbank' IS USED TO REFER TO THE REDIS DATABASE THAT
        STORES ALL OF THE SONG DATA.

        Args:
            (Varies between methods)
            index (int): An index at which to start searching through the songlist.
            data (list[dict]): A list of dictionaries containing the data of a song.
            name (str): The name of a song in the songbank.
   
        Returns:
            result (list/str): Varies between methods
        '''
        # READ
        # route should be able to retrieve song data from redis
        # be able to to retrieve entire songbank, from given index, or a single song
        if(request.method == 'GET'):
            def data_out(index = 0):
                '''
                Iterates through the data in the Redis server and returns a list
                of song data. Can start iterating from a user-given index.

                Args:
                    searchIndex (int): An index at which to start iterating through the
                                       database at.

                Returns:
                    songbank (dict): A jsonified dictionary containing song data.
                '''
                n_keys = len(rd3.keys())
                if(n_keys == 0):
                    return 'Database empty. To add a song, use the POST method.'
                else:
                    songbank = {}
                    for i in range(index, n_keys):
                        songbank[str(i)] = rd3.get(str(i))
                    return jsonify(songbank)


        # CREATE
        # route to create new data to input into the database
        if(request.method == 'POST'):
            def data_in(data):
                '''
                Takes a user-given song-data object and uploads it to the Redis
                songbank.

                Args:
                    data (list[dict]): A list of dictionaries containing data of a song.

                Returns:
                    str: A confirmation message if the upload is successful.
                '''
                ###################################################### insert a check here to make sure it's a list or mp object
                rd3.set(str(len(rd3.keys())), data)
                return 'Successfully uploaded song.'



        # UPDATE
        # update a song by replacing it with a user-uploaded version of the same name
        if(request.method == 'PUT'):
            def data_replace(data):
                '''
                Replaces a song-data object in the Redis database with its user-given namesake.

                Args:
                    data (list[dict]): A list of dictionaries containing data for a song.

                Returns:
                    str: A confirmation message that the update was a success.
                '''
                ################################################### insert a check that the given song has a name key/value
                n_keys = len(rd3.keys())
                dataName = data['name']
                for i in range(0, n_keys):
                    searchName = rd3.get(str(i))['name']
                    if(searchName.lower() == dataName.lower()):
                        rd3.set(search['name'], data)
                        return 'Successfully updated song.'
                return 'No song of that name in database.'



        # DELETE
        # delete a specific song from the songbank
        if(request.method == 'DELETE'):
            def data_delete(name):
                '''
                Takes a song name and deletes that song from the songbank.

                Args:
                    name (str): The name of the song to be removed from the Redis database.

                Returns:
                    str: A confirmation message
                '''
                n_keys = len(rd3.keys())
                for i in range(0, n_keys):
                    to_delete = rd3.get(str(i))
                    delName = to_delete['name']
                    if( delName.lower() == name.lower()):
                        rd3.remove(str(i))
                        return 'Successfully deleted.'
                return 'Song not in database.'







    
