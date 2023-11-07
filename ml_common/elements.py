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
        self.first_element: Text = elements[0]
        self.elements = elements

        joined_metadata = self.first_element.metadata
        # check if this needs more metadata joining
        for element in elements[1:]:
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

        super().__init__(
            text=sep_txt.join([e.text for e in elements]),
            element_id=self.first_element.id,
            metadata=joined_metadata,
        )
