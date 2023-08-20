from model.vegetableStorage import VegetableStorage


# Author:Xiaoping Zhang
# Date: July 22, 2023


class Cabbage(VegetableStorage):

    def get_description(self):
        return '''Cabbage, comprising several cultivars of Brassica oleracea, is a leafy green, red (purple), or white (pale green) biennial plant grown as an annual vegetable crop for its dense-leaved heads. It is descended from the wild cabbage (B. oleracea var. oleracea), and belongs to the "cole crops" or brassicas, meaning it is closely related to broccoli and cauliflower (var. botrytis); Brussels sprouts (var. gemmifera); and Savoy cabbage (var. sabauda).'''

class Onion(VegetableStorage):

    def get_description(self):
        return '''An onion (Allium cepa L., from Latin cepa meaning "onion"), also known as the bulb onion or common onion, is a vegetable that is the most widely cultivated species of the genus Allium. The shallot is a botanical variety of the onion which was classified as a separate species until 2011.[2][3]: 21  Its close relatives include garlic, scallion, leek, and chive.[4]'''

class Carrot(VegetableStorage):

    def get_description(self):
        return '''The carrot (Daucus carota subsp. sativus) is a root vegetable, typically orange in color, though purple, black, red, white, and yellow cultivars exist,[2][3][4] all of which are domesticated forms of the wild carrot, Daucus carota, native to Europe and Southwestern Asia. The plant probably originated in Persia and was originally cultivated for its leaves and seeds. The most commonly eaten part of the plant is the taproot, although the stems and leaves are also eaten. The domestic carrot has been selectively bred for its enlarged, more palatable, less woody-textured taproot.'''

class Potato(VegetableStorage):

    def get_description(self):
        return '''The potato is a starchy food, a tuber of the plant Solanum tuberosum and is a root vegetable native to the Americas. The plant is a perennial in the nightshade family Solanaceae.[2]'''

class Rutabaga(VegetableStorage):

    def get_description(self):
        return '''Rutabaga (/ˌruːtəˈbeɪɡə/; North American English) or swede (English English and some Commonwealth English) is a root vegetable, a form of Brassica napus (which also includes rapeseed). Other names include Swedish turnip, neep (Scots), and turnip (Scottish and Canadian English, Irish English and Manx English). However, elsewhere the name "turnip" usually refers to the related white turnip. The species Brassica napus originated as a hybrid between the cabbage (Brassica oleracea) and the turnip (Brassica rapa). Rutabaga roots are eaten as human food in various ways, and the leaves can be eaten as a leaf vegetable. The roots and tops are also used for livestock, either fed directly in the winter or foraged in the field during the other seasons. Scotland, Northern and Western England, Wales, the Isle of Man and Ireland had a tradition of carving the roots into lanterns at Halloween.'''


if __name__ == '__main__':
    param = [i for i in range(16)]
    a = Cabbage(*param)
    tmp = []
    for i in [Cabbage, Onion, Rutabaga, Potato]:
        print('****************')
        print(i(*param).get_description())