from dataclasses import dataclass
from typing import Any

import yaml
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class PersonalInformation(BaseModel):
    name: str | None
    surname: str | None
    date_of_birth: str | None
    country: str | None
    city: str | None
    address: str | None
    zip_code: str | None = Field(None, min_length=5, max_length=10)
    phone_prefix: str | None
    phone: str | None
    email: EmailStr | None
    github: HttpUrl | None = None
    linkedin: HttpUrl | None = None


class EducationDetails(BaseModel):
    education_level: str | None
    institution: str | None
    field_of_study: str | None
    final_evaluation_grade: str | None
    start_date: str | None
    year_of_completion: int | None
    exam: list[dict[str, str]] | dict[str, str] | None = None


class ExperienceDetails(BaseModel):
    position: str | None
    company: str | None
    employment_period: str | None
    location: str | None
    industry: str | None
    key_responsibilities: list[dict[str, str]] | None = None
    skills_acquired: list[str] | None = None


class Project(BaseModel):
    name: str | None
    description: str | None
    link: HttpUrl | None = None


class Achievement(BaseModel):
    name: str | None
    description: str | None


class Certifications(BaseModel):
    name: str | None
    description: str | None


class Language(BaseModel):
    language: str | None
    proficiency: str | None


class Availability(BaseModel):
    notice_period: str | None


class SalaryExpectations(BaseModel):
    salary_range_usd: str | None


class SelfIdentification(BaseModel):
    gender: str | None
    pronouns: str | None
    veteran: str | None
    disability: str | None
    ethnicity: str | None


class LegalAuthorization(BaseModel):
    eu_work_authorization: str | None
    us_work_authorization: str | None
    requires_us_visa: str | None
    requires_us_sponsorship: str | None
    requires_eu_visa: str | None
    legally_allowed_to_work_in_eu: str | None
    legally_allowed_to_work_in_us: str | None
    requires_eu_sponsorship: str | None


class Resume(BaseModel):
    personal_information: PersonalInformation | None
    education_details: list[EducationDetails] | None = None
    experience_details: list[ExperienceDetails] | None = None
    projects: list[Project] | None = None
    achievements: list[Achievement] | None = None
    certifications: list[Certifications] | None = None
    languages: list[Language] | None = None
    interests: list[str] | None = None

    @staticmethod
    def normalize_exam_format(exam):
        if isinstance(exam, dict):
            return [{k: v} for k, v in exam.items()]
        return exam

    def __init__(self, yaml_str: str):
        try:
            # Parse the YAML string
            data = yaml.safe_load(yaml_str)

            if "education_details" in data:
                for ed in data["education_details"]:
                    if "exam" in ed:
                        ed["exam"] = self.normalize_exam_format(ed["exam"])

            # Create an instance of Resume from the parsed data
            super().__init__(**data)
        except yaml.YAMLError as e:
            raise ValueError("Error parsing YAML file.") from e
        except Exception as e:
            raise Exception(f"Unexpected error while parsing YAML: {e}") from e

    def _process_personal_information(self, data: dict[str, Any]) -> PersonalInformation:
        try:
            return PersonalInformation(**data)
        except TypeError as e:
            raise TypeError(f"Invalid data for PersonalInformation: {e}") from e
        except AttributeError as e:
            raise AttributeError(f"AttributeError in PersonalInformation: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error in PersonalInformation processing: {e}") from e

    def _process_education_details(self, data: list[dict[str, Any]]) -> list[EducationDetails]:
        education_list = []
        for edu in data:
            try:
                exams = [Exam(name=k, grade=v) for k, v in edu.get("exam", {}).items()]
                education = EducationDetails(
                    education_level=edu.get("education_level"),
                    institution=edu.get("institution"),
                    field_of_study=edu.get("field_of_study"),
                    final_evaluation_grade=edu.get("final_evaluation_grade"),
                    start_date=edu.get("start_date"),
                    year_of_completion=edu.get("year_of_completion"),
                    exam=exams,
                )
                education_list.append(education)
            except KeyError as e:
                raise KeyError(f"Missing field in education details: {e}") from e
            except TypeError as e:
                raise TypeError(f"Invalid data for Education: {e}") from e
            except AttributeError as e:
                raise AttributeError(f"AttributeError in Education: {e}") from e
            except Exception as e:
                raise Exception(f"Unexpected error in Education processing: {e}") from e
        return education_list

    def _process_experience_details(self, data: list[dict[str, Any]]) -> list[ExperienceDetails]:
        experience_list = []
        for exp in data:
            try:
                key_responsibilities = [
                    Responsibility(description=list(resp.values())[0])
                    for resp in exp.get("key_responsibilities", [])
                ]
                skills_acquired = [str(skill) for skill in exp.get("skills_acquired", [])]
                experience = ExperienceDetails(
                    position=exp["position"],
                    company=exp["company"],
                    employment_period=exp["employment_period"],
                    location=exp["location"],
                    industry=exp["industry"],
                    key_responsibilities=key_responsibilities,
                    skills_acquired=skills_acquired,
                )
                experience_list.append(experience)
            except KeyError as e:
                raise KeyError(f"Missing field in experience details: {e}") from e
            except TypeError as e:
                raise TypeError(f"Invalid data for Experience: {e}") from e
            except AttributeError as e:
                raise AttributeError(f"AttributeError in Experience: {e}") from e
            except Exception as e:
                raise Exception(f"Unexpected error in Experience processing: {e}") from e
        return experience_list


@dataclass
class Exam:
    name: str
    grade: str


@dataclass
class Responsibility:
    description: str
