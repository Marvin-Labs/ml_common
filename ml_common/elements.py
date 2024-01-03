from unstructured.documents.elements import *


class LinearTextCombination(Text):
    """A linear combination of text elements."""

    JOIN_METADATA_ELEMENTS = ["section"]
    JOIN_METADATA_SEP = ","

    def __init__(
        self,
        elements: list[Text],
        sep_txt: str = " ",
    ):
        assert len(elements) > 0, "Must have at least one element"
        # we are looking through other LinearTextCombinations
        self.elements = list()
        for e in elements:
            if isinstance(e, LinearTextCombination):
                self.elements += e.elements
            else:
                self.elements.append(e)

        self.first_element: Text = self.elements[0]
        self._sep_txt = sep_txt

        super().__init__(
            text=self._joined_text(),
            element_id=self.first_element.id,
            metadata=self._joined_metadata(),
        )

    def _joined_metadata(self):
        joined_metadata = self.first_element.metadata
        # check if this needs more metadata joining
        for element in self.elements[1:]:
            for jme in self.JOIN_METADATA_ELEMENTS:
                if (meta_element := getattr(element.metadata, jme)) is not None:
                    current_value = getattr(joined_metadata, jme)
                    if current_value is None:
                        setattr(joined_metadata, jme, meta_element)
                    else:
                        setattr(
                            joined_metadata,
                            jme,
                            current_value + self.JOIN_METADATA_SEP + meta_element,
                        )
        return joined_metadata

    def _joined_text(self) -> str:
        return self._sep_txt.join([e.text for e in self.elements])

    def refresh(self):
        self.text = self._joined_text()
        self.metadata = self._joined_metadata()

    def append(self, element: Text):
        if isinstance(element, LinearTextCombination):
            for e in element.elements:
                self.append(e)

        else:
            self.elements.append(element)

        self.refresh()