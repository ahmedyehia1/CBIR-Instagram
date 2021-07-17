from flask import Flask,render_template,request,send_from_directory
from os import path,mkdir
from werkzeug.utils import secure_filename
from instagram_app import *
from shutil import move
from pathlib import Path

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static/uploads"

# global list to show 
shownItems = []
# global list with avalible usernames 
globalUsername = []



@app.route("/instagram")
def GetInstagram():
    return render_template("instagram.html",maxShownImages=None)


def show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name,indecis=None,maxShownImages=True):
    if(indecis == None):
        for x in range(len(image_instagramLinks)):
            shownItems.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})
    else:
        for x in range(len(image_instagramLinks)):
            if(x in indecis):
                shownItems.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})

    print(shownItems)
    if maxShownImages:
        return render_template("instagram.html",results=shownItems,maxShownImages=len(shownItems))
    else:
        return render_template("instagram.html",results=shownItems,maxShownImages=None)

@app.route('/instagram/imageSimilarity',methods=['POST'])
def uploadI2():
    file = request.files.get("file")
    print(file)
    filename = secure_filename(file.filename)
    file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
    queryImage = path.join(app.config['UPLOAD_FOLDER'], filename)
    print(queryImage)
    # for file in files:
    #         filename = secure_filename(file.filename)
    #         file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
    #         queryImage = path.join(app.config['UPLOAD_FOLDER'], filename)
    #         break


    #retrive all data
    image_instagramLinks, image_paths, image_descriptions, image_featureVectors, store_name = get_history_data("dataset.p")
    
    query_features = prepare_query_image(queryImage)

    #get similar images
    shownImages = request.form.get("resCount")
    print(type(shownImages))
    shownImages = int(shownImages)
    print(type(shownImages))
    similar_images_indices = get_closest_images(query_features, image_featureVectors, shownImages)

    global shownItems
    shownItems = []
    return show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name,similar_images_indices)


@app.route('/instagram/store',methods=['POST'])
def getAllItems_route():

    global shownItems
    global globalUsername

    username = request.form.getlist("username")
    
    if set(username)-set(globalUsername):
        # update showItems if new username is added
        ############################
        ######## model code ########
        ############################
        posts_lists = [[], [], [], [] , []]

        for user in username:
            #get images from instagram
            posts = get_username(user)

            print(posts)
            #make a list for each post variable
            for x in posts:
                posts_lists[0].append(x.image_instagramLink)
                posts_lists[1].append(x.image_path)
                posts_lists[2].append(x.image_description)
                posts_lists[4].append(user)
                
        print("before prepare",posts_lists)

        #get feature vector of images
        posts_lists = prepare_dataset(posts_lists)

        print("not gonna run")

        #save the dataset
        save_dataset(posts_lists)

        #retrive all data
        image_instagramLinks, image_paths, image_descriptions, image_featureVectors, store_name = get_history_data("dataset.p")
        

        # global shownItems
        shownItems = []



        # for x in range(len(image_instagramLinks)):
        #     shownItems.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})

        #query image get feature vector of image
        
        # print(len(query_features))


        

        # links = []
        # # #get similar images links
        # for x in similar_images_indices:
        #     links.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})

        for user in username:
            if Path(path.join(app.config['UPLOAD_FOLDER'], user)).is_dir() == False:
                move(user,path.join(app.config['UPLOAD_FOLDER'], user))
        
        globalUsername = username
        
        return show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name)

    if set(globalUsername)-set(username):
        # update showItems if a username was deleted
        newShownItems = []
        for item in shownItems:
            if item['username'] in username:
                newShownItems.append(item)

        shownItems = newShownItems
        globalUsername = username
        
    
    return render_template("instagram.html",results=shownItems,maxShownImages=len(shownItems))
    
    

@app.route('/instagram/filter',methods=['POST'])
def uploadIupdate():

    username = request.form.getlist("username")
    # print(username)
    # posts_lists = [[], [], [], [] , []]

    # for user in username:
    #     #get images from instagram
    #     posts = get_username(user)

    #     #make a list for each post variable
    #     for x in posts:
    #         posts_lists[0].append(x.image_instagramLink)
    #         posts_lists[1].append(x.image_path)
    #         posts_lists[2].append(x.image_description)
    #         posts_lists[4].append(user)
            

    # #get feature vector of images
    # posts_lists = prepare_dataset(posts_lists)

    # #save the dataset
    # save_dataset(posts_lists)

    # #retrive all data
    # image_instagramLinks, image_paths, image_descriptions, image_featureVectors, store_name = get_history_data("dataset.p")
    

    # for x in range(len(image_instagramLinks)):
    #     shownItems.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})

    #query image get feature vector of image
    
    # print(len(query_features))


    

    # links = []
    # # #get similar images links
    # for x in similar_images_indices:
    #     links.append({"username":store_name[x],"link":image_instagramLinks[x],"img":path.join(app.config['UPLOAD_FOLDER'], image_paths[x]),"desc":image_descriptions[x]})

    for user in username:
        if Path(path.join(app.config['UPLOAD_FOLDER'], user)).is_dir() == False:
            move(user,path.join(app.config['UPLOAD_FOLDER'], user))
    # print(links)
    return render_template("instagram.html",results=shownItems)
    # show_retrival_items(image_instagramLinks, image_paths, image_descriptions, store_name)
    

if __name__ == "__main__":
    app.run()