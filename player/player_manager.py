class Player:

    def __init__(
        self,
        player_type,
        name,
        identifier
    ):

        self.player_type = player_type
        self.name = name
        self.identifier = identifier

    def get_display_identity(self):

        return (
            f"{self.name}_{self.identifier}"
        )

    def get_registration_key(self):

        return (
            f"{self.player_type}:"
            f"{self.identifier}"
        )


class PlayerManager:

    EMPLOYEE = "EMPLOYEE"
    EXTERNAL = "EXTERNAL"

    def __init__(self):

        self.current_player = None

    def create_player(
        self,
        player_type,
        name,
        identifier
    ):

        player_type = self._normalize_player_type(
            player_type
        )

        name = self._normalize_name(
            name
        )

        identifier = self._normalize_identifier(
            identifier
        )

        self._validate_player(
            player_type,
            name,
            identifier
        )

        self.current_player = Player(
            player_type,
            name,
            identifier
        )

        return self.current_player

    def _normalize_player_type(
        self,
        player_type
    ):

        return player_type.strip().upper()

    def _normalize_name(
        self,
        name
    ):

        return " ".join(
            name.strip().split()
        )

    def _normalize_identifier(
        self,
        identifier
    ):

        return identifier.strip()

    def _validate_player(
        self,
        player_type,
        name,
        identifier
    ):

        if player_type not in (
            self.EMPLOYEE,
            self.EXTERNAL
        ):

            raise ValueError(
                "Invalid player type."
            )

        if not name:

            raise ValueError(
                "Player name is required."
            )

        if not identifier:

            raise ValueError(
                "Player identifier is required."
            )

        if (
            player_type == self.EMPLOYEE
            and not identifier.isdigit()
        ):

            raise ValueError(
                "Employee Staff ID must contain "
                "digits only."
            )

        if (
            player_type == self.EMPLOYEE
            and len(identifier) != 6
        ):

            raise ValueError(
                "Employee Staff ID must be "
                "exactly 6 digits."
            )

    def get_current_player(self):

        return self.current_player