class EnergyComputationError(RuntimeError):
    """Raised when an error occurs during energy computation processes."""

    pass


class NpvComputationError(RuntimeError):
    """Raised when the Net Present Value (NPV) calculation fails or produces invalid results."""

    pass


class LcoeComputationError(RuntimeError):
    """Raised when the Levelized Cost of Energy (LCOE) computation encounters an error."""

    pass


class ReadDeviationError(RuntimeError):
    """Raised when there is an issue reading deviation data from input sources."""

    pass


class ReadSimulationDataError(RuntimeError):
    """Raised when simulation data cannot be read or parsed correctly."""

    pass
