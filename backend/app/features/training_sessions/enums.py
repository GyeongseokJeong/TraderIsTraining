from enum import StrEnum


class TrainingSessionStatus(StrEnum):
    setup = "SETUP"
    running = "RUNNING"
    finished = "FINISHED"


class TrainingSessionMode(StrEnum):
    personal_review = "PERSONAL_REVIEW"
