import json
from collections import UserDict
from typing import Any
from typing import NoReturn
from typing import Optional

from moviefinder.item import Item
from moviefinder.resources import sample_movies_json_path
from moviefinder.user import user


class Items(UserDict):
    """A singleton dictionary of movies and shows.

    The keys are IDs and the values are Item objects.
    """

    __instance: Optional["Items"] = None

    def __new__(cls) -> "Items":
        if cls.__instance is None:
            cls.__instance = super(Items, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()

    def __copy__(self) -> NoReturn:
        raise RuntimeError("The Items singleton object cannot be copied.")

    def __deepcopy__(self, _) -> NoReturn:
        raise RuntimeError("The Items singleton object cannot be copied.")

    def load(self) -> Optional[bool]:
        """Loads movies and shows from the service.

        Assumes the user object has already been loaded and has valid data. Returns True
        if the items were loaded successfully. Returns None if unable to get a valid
        response from the service. Returns False if the service's response was valid but
        there are no movies or shows to display after filtering.
        """
        if self.data:
            raise RuntimeError(
                "Cannot load items when they are already loaded."
                " Use the clear function if needed."
            )
        # TODO
        # response = requests.get(
        #     url="https://chuadevs.com:1587/v1/movie/",
        #     params={
        #         "country": user.region.name.lower(),
        #         "service": [service.value.lower() for service in user.services],
        #         "genre": ["Action","Comedy"],
        #         "page": 1,
        #         "orderBy": "original_title"
        #           # (a string that is either "original_title" or "year")
        #     },
        # )
        # if not response:
        #     return None
        # response.encoding = "utf-8"
        # response_dict = response.json()
        # # total_pages: int = response_dict["total_pages"]  # TODO
        # items_data: list[dict] = response_dict["results"]
        # print("Loading items...")
        # for item_data in items_data:
        #     new_item = Item(item_data)
        #     if self.__service_and_region_match(new_item):
        #         self.data[new_item.id] = new_item
        # return bool(self.data)

        with open(sample_movies_json_path, "r", encoding="utf8") as file:
            service_obj: dict[str, Any] = json.load(file)
            # total_pages: int = service_obj["total_pages"]
            items_data: list[dict] = service_obj["movies"]
            print("Loading items...")
            for item_data in items_data:
                new_item = Item(item_data)
                if self.__service_and_region_match(new_item):
                    self.data[new_item.id] = new_item
        return bool(self.data)

    def __service_and_region_match(self, item: Item) -> bool:
        """Checks if the user has the service & region of the item."""
        if user.region not in item.regions:
            print(
                f"\t{item.title} not added because {user.region} not in {item.regions}."
            )
            return False
        for service in user.services:
            if service in item.services:
                return True
        print(
            f"\t{item.title} not added because {user.services} ⋂ {item.services} = Ø."
        )
        return False


items = Items()