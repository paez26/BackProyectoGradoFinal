# from nutree import Tree, Node
# import os
# import subprocess
# path ="repos/Group22-MobileApp-Grupo22-Kotlin/app/src/main/java/com/example"
# tree = Tree("Moviles")
# list = []

# david = []

# contador = "0"

# os.environ['PATH'] += os.pathsep + r'C:\Graphviz-11.0.0-win64\bin'

# def aumentar():
#     global contador
#     contador = str(int(contador)+1)
#     return contador

# def createbranch(path, node):
#     for file in os.listdir(path):
       
#         if file not  in david and file.__contains__("."):
#             p = node.add(file+"_"+aumentar())
#         if not file.__contains__("."):
#             p = node.add(file+"_"+aumentar())
#             createbranch(path+"/"+file, p)
    
# createbranch(path+"/", tree)
    
        
# output_dir = "photos"
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# # Save the DOT file
# dotfile_path = os.path.join(output_dir, "tree_structure.gv")
# tree.to_dotfile(dotfile_path)

# # Convert the DOT file to a PNG image using Graphviz
# png_path = os.path.join(output_dir, "tree_structure.png")
# subprocess.run(["dot", "-Tpng", dotfile_path, "-o", png_path])


