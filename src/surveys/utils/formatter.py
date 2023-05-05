from surveys.models import Question, QuestionAnswer


def singleCustomerFormatter(customer):
    singleCustomer = {}

    singleCustomer["id"] = customer.pk
    singleCustomer["name"] = customer.name
    singleCustomer["description"] = customer.description
    singleCustomer["location"] = customer.location
    singleCustomer["contact"] = customer.contact

    return singleCustomer


def multipleCustomerFormatter(customers):
    allCustomers = []
    for customer in customers:
        singleCustomer = {}

        singleCustomer["id"] = customer.pk
        singleCustomer["name"] = customer.name
        singleCustomer["description"] = customer.description
        singleCustomer["location"] = customer.location
        singleCustomer["contact"] = customer.contact

        allCustomers.append(singleCustomer)

    return allCustomers


def singleProjectFormatter(project):
    singleProject = {}

    singleProject["id"] = project.pk
    singleProject["name"] = project.name
    singleProject["description"] = project.description
    singleProject["customer_id"] = project.customer.pk
    singleProject["customer_name"] = project.customer.name
    singleProject["date"] = project.date
    singleProject["location"] = project.location
    singleProject["noOfDataCollectors"] = project.noOfDataCollectors
    singleProject["budget"] = project.budget

    return singleProject


def multipleProjectFormatter(projects):
    allProjects = []

    for project in projects:
        singleProject = {}

        singleProject["id"] = project.pk
        singleProject["name"] = project.name
        singleProject["description"] = project.description
        singleProject["customer_id"] = project.customer.pk
        singleProject["customer_name"] = project.customer.name
        singleProject["date"] = project.date
        singleProject["location"] = project.location
        singleProject["noOfDataCollectors"] = project.noOfDataCollectors
        singleProject["budget"] = project.budget

        allProjects.append(singleProject)

    return allProjects


def singleSurveyFormatter(survey):
    singleSurvey = {}

    singleSurvey["id"] = survey.id
    singleSurvey["name"] = survey.name
    singleSurvey["project_id"] = survey.project.pk
    singleSurvey["project_name"] = survey.project.name
    singleSurvey["description"] = survey.description
    singleSurvey["status"] = survey.status
    singleSurvey["language"] = survey.language

    singleSurvey["language"] = survey.language.name

    all_categories = []
    for cat in survey.categories.all():
        singleCategory = {}
        singleCategory["name"] = cat.name
        singleCategory["id"] = cat.id

        all_categories.append(singleCategory)

    singleSurvey["categories"] = all_categories

    allDataCollectors = []
    for user in survey.dataCollectors.all():
        singleDataCollector = {}
        singleDataCollector["first_name"] = user.first_name
        singleDataCollector["last_name"] = user.last_name
        singleDataCollector["id"] = user.id

        allDataCollectors.append(singleDataCollector)

    singleSurvey["dataCollectors"] = allDataCollectors

    return singleSurvey


def multipleSurveyFormatter(surveys):
    allSurveys = []

    for survey in surveys:
        singleSurvey = {}

        singleSurvey["id"] = survey.pk
        singleSurvey["name"] = survey.name
        singleSurvey["project_id"] = survey.project.pk
        singleSurvey["project_name"] = survey.project.name
        singleSurvey["description"] = survey.description
        singleSurvey["status"] = survey.status

        singleSurvey["language"] = survey.language.name

        all_categories = []
        for cat in survey.categories.all():
            singleCategory = {}
            singleCategory["name"] = cat.name
            singleCategory["id"] = cat.id

            all_categories.append(singleCategory)

        singleSurvey["categories"] = all_categories

        allDataCollectors = []
        for user in survey.dataCollectors.all():
            singleDataCollector = {}
            singleDataCollector["first_name"] = user.first_name
            singleDataCollector["last_name"] = user.last_name
            singleDataCollector["id"] = user.id

            allDataCollectors.append(singleDataCollector)

        singleSurvey["dataCollectors"] = allDataCollectors

        allSurveys.append(singleSurvey)

    return allSurveys


def singleSurveyWithQuestions(survey):
    singleSurvey = {}

    singleSurvey["pk"] = survey.pk
    singleSurvey["name"] = survey.name
    singleSurvey["project_id"] = survey.project.pk
    singleSurvey["project_name"] = survey.project.name
    singleSurvey["description"] = survey.description
    singleSurvey["status"] = survey.status
    singleSurvey["language"] = survey.language.name

    all_categories = []
    for cat in survey.categories.all():
        singleCategory = {}
        singleCategory["name"] = cat.name
        singleCategory["id"] = cat.id

        all_categories.append(singleCategory)

    singleSurvey["categories"] = all_categories

    allDataCollectors = []
    for user in survey.dataCollectors.all():
        singleDataCollector = {}
        singleDataCollector["first_name"] = user.first_name
        singleDataCollector["last_name"] = user.last_name
        singleDataCollector["email"] = user.email
        singleDataCollector["phone"] = user.phone
        singleDataCollector["id"] = user.id

        allDataCollectors.append(singleDataCollector)

    singleSurvey["dataCollectors"] = allDataCollectors

    surveyQuestions = Question.objects.filter(survey=survey)

    singleSurvey["questions"] = []

    for question in surveyQuestions:
        singleQuestion = {}
        singleQuestion["id"] = question.pk
        singleQuestion["title"] = question.title
        singleQuestion["hasMultipleAnswers"] = question.hasMultipleAnswers
        singleQuestion["isRequired"] = question.isRequired
        singleQuestion["type"] = question.type
        singleQuestion["options"] = question.options
        singleQuestion["isDependent"] = question.isDependent
        singleQuestion["depQuestion"] = question.depQuestion
        singleQuestion["audioURL"] = question.audioURL
        singleQuestion["imageURL"] = question.imageURL
        singleQuestion["videoURL"] = question.videoURL

        all_categories = []

        singleCategory = {}
        singleCategory["name"] = question.category.name
        singleCategory["id"] = question.category.pk

        all_categories.append(singleCategory)

        singleQuestion["categories"] = all_categories
        singleQuestion["answers"] = questionAnswerFormatter(question.pk)

        singleSurvey["questions"].append(singleQuestion)

    return singleSurvey


def questionAnswerFormatter(question_id):
    getAnswers = QuestionAnswer.objects.filter(question__id=question_id)

    allAnswers = []
    for answer in getAnswers:
        singleAnswer = {}
        singleAnswer["id"] = answer.pk
        singleAnswer["createdAt"] = answer.createdAt
        singleAnswer["responses"] = answer.responses
        singleAnswer["location"] = answer.location

        allAnswers.append(singleAnswer)

    return allAnswers


def multipleQuestionFormatter(questions):
    allQuestions = []
    for question in questions:
        singleQuestion = {}
        singleQuestion["id"] = question.pk
        singleQuestion["title"] = question.title
        singleQuestion["hasMultipleAnswers"] = question.hasMultipleAnswers
        singleQuestion["isRequired"] = question.isRequired
        singleQuestion["type"] = question.type
        singleQuestion["options"] = question.options
        singleQuestion["isDependent"] = question.isDependent
        singleQuestion["depQuestion"] = question.depQuestion
        singleQuestion["audioURL"] = question.audioURL
        singleQuestion["imageURL"] = question.imageURL
        singleQuestion["videoURL"] = question.videoURL

        allQuestions.append(singleQuestion)

    return allQuestions
