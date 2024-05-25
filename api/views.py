from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse 
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from .models import *
from .serializers import *
from http import HTTPStatus 
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status



# Create a new user
@api_view(['POST'])
def create_user(request):
    # Get the username and password from the request data
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Validate that both username and password are provided
    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    # Create a new user with the provided username and password
    user = User.objects.create_user(username=username, password=password)
    
    # Serialize the user data to include only the username
    user_data = {'username': user.username}
    return JsonResponse({'message': 'User account created successfully', 'user': user_data}, status=201)

# Log in as a user
@api_view(['POST'])
@csrf_exempt
def user_login(request):
    # Get the username and password from the request data
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Validate that both username and password are provided
    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)
    
    # Authenticate the user
    user = authenticate(request, username=username, password=password)
    
    # If the user is authenticated, log them in and return a success message
    if user is not None:
        login(request, user)
        user_data = {'username': user.username}
        return JsonResponse({'message': 'Login successful', 'user': user_data}, status=200)
    else:
        # If authentication fails, return an error message
        return JsonResponse({'error': 'Invalid credentials'}, status=400)


# Create a learner account
@api_view(['POST','PUT'])
@csrf_exempt
def create_learner(request):
    user = request.user
    try:
        learner = Learner.objects.get(user=user)
    except Learner.DoesNotExist:
        learner = None
    request.data['user'] = request.user.id
    if request.method == 'POST':
        serializer = LearnerSerializer(data=request.data)
        
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create an educator account
@api_view(['POST'])
@csrf_exempt
def create_educator(request):
    user = request.user
    name = request.data.get('name')
    description = request.data.get('description')
    charges = request.data.get('charges')
    tags_data = request.data.get('tags', [])  # Get tags data as a list or empty list if not provided

    # Check if the user already has an associated educator account
    if Educator.objects.filter(user=user).exists():
        return JsonResponse({'error': 'User already has an educator account'}, status=400)

    # Validate and associate tags with the educator account
    tags = []
    for tag_name in tags_data:
        try:
            tag = Tag.objects.get(name=tag_name)
            tags.append(tag)
        except Tag.DoesNotExist:
            return JsonResponse({'error': f'Tag "{tag_name}" does not exist'}, status=400)

    # Create the educator account
    educator = Educator.objects.create(user=user, name=name, description=description, charges=charges)
    educator.tags.set(tags)  # Set the tags for the educator account

    # Serialize the educator data
    educator_serializer = EducatorSerializer(educator)
    return JsonResponse({'message': 'Educator account created successfully', 'educator': educator_serializer.data}, status=201)

# Make a session request
@api_view(['POST'])
@csrf_exempt
def make_session_request(request):
    user = request.user

    # Ensure the request is made by a learner
    try:
        learner = Learner.objects.get(user=user)
    except Learner.DoesNotExist:
        return JsonResponse({'error': 'Only learners can create session requests'}, status=status.HTTP_403_FORBIDDEN)

    # Get the educator ID, duration, price, and problem description from the request data
    educator_id = request.data.get('educator_id')
    duration = request.data.get('duration')
    price = request.data.get('price')
    problem_description = request.data.get('problem_description')

    # Validate educator
    try:
        educator = Educator.objects.get(id=educator_id)
    except Educator.DoesNotExist:
        return JsonResponse({'error': 'Educator not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get the tags from the educator
    tags = educator.tags.all()

    # Create the session
    session = Session.objects.create(
        learner=learner,
        educator=educator,
        duration=duration,
        price=price,
        problem_description=problem_description,
        session_status='sent',
        payment_status='pending'
    )
    session.tags.set(tags)  # Set the tags for the session

    # Serialize the session data
    session_serializer = SessionSerializer(session)
    return JsonResponse({'message': 'Session request created successfully', 'session': session_serializer.data}, status=status.HTTP_201_CREATED)


 # Review list of session requests made to a specific educator
@api_view(['GET'])
def get_educator_sessions(request):
    user = request.user

    # Ensure the request is made by an educator
    try:
        educator = Educator.objects.get(user=user)
    except Educator.DoesNotExist:
        return JsonResponse({'error': 'Only educators can make requests'}, status=status.HTTP_403_FORBIDDEN)

    # Fetch sessions for the logged-in educator
    sessions = Session.objects.filter(educator=educator)
    session_serializer = SessionSerializer(sessions, many=True)
    return JsonResponse({'sessions': session_serializer.data}, status=status.HTTP_200_OK)


# Review the list and status of session requests made by a specific learner
@api_view(['GET'])
def get_learner_sessions(request):
    user = request.user

    # Ensure the request is made by a learner
    try:
        learner = Learner.objects.get(user=user)
    except Learner.DoesNotExist:
        return JsonResponse({'error': 'Only learners can make requests'}, status=status.HTTP_403_FORBIDDEN)

    # Fetch sessions for the logged-in learner
    sessions = Session.objects.filter(learner=learner)
    session_serializer = SessionSerializer(sessions, many=True)
    return JsonResponse({'sessions': session_serializer.data}, status=status.HTTP_200_OK)

# Accept/reject the session request
@api_view(['POST'])
@csrf_exempt
def update_session_status(request, session_id):
    status = request.data.get('status')  # 'accepted' or 'rejected'
    try:
        session = Session.objects.get(id=session_id)
        session.session_status= status
        session.save()
        session_serializer = SessionSerializer(session)
        return JsonResponse({'message': 'Session status updated successfully' , 'status' : session_serializer.data}, status=HTTPStatus.OK)
    except Session.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=HTTPStatus.NOT_FOUND)

# Delete the session
@api_view(['DELETE'])
def delete_session(request, session_id):
    try:
        session = Session.objects.get(id=session_id)
        session.delete()
        return JsonResponse({'message': 'Session deleted successfully'}, status=HTTPStatus.OK)
    except Session.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=HTTPStatus.NOT_FOUND)

# List all the sessions + reviews of the educator
@api_view(['GET'])
def list_educator_sessions_and_reviews(request, educator_id):
    sessions = Session.objects.filter(educator_id=educator_id)
    session_serializer = SessionSerializer(sessions, many=True)
    
    reviews = Review.objects.filter(session__educator_id=educator_id)
    review_serializer = ReviewSerializer(reviews, many=True)
    
    return JsonResponse({
        'sessions': session_serializer.data,
        'reviews': review_serializer.data
    }, status=HTTPStatus.OK)


# List all learners with their details
@api_view(['GET'])
def list_learners(request):
    learners = Learner.objects.all()
    learner_serializer = LearnerSerializer(learners, many=True)
    return Response(learner_serializer.data, status=status.HTTP_200_OK)

# List all educators with their details
@api_view(['GET'])
def list_educators(request):
    educators = Educator.objects.all()

    # Manually serialize the educators with tag names
    educator_data = []
    for educator in educators:
        # Fetch tag names for each educator
        tag_names = [tag.name for tag in educator.tags.all()]

        # Serialize the educator data
        educator_data.append({
            'id': educator.id,
            'name': educator.name,
            'tags': tag_names,  # Include tag names instead of IDs
            'description': educator.description,
            'charges': educator.charges
        })

    return Response(educator_data, status=status.HTTP_200_OK)

# List all the tags
@api_view(['GET'])
def list_tags(request):
    tags = Tag.objects.all()
    tag_serializer = TagSerializer(tags , many = True)
    return Response(tag_serializer.data , status=status.HTTP_200_OK)


@api_view(['POST'])
def add_review(request):
    user = request.user
    
    # Check if the user is a learner
    try:
        learner = Learner.objects.get(user=user)
    except Learner.DoesNotExist:
        return Response({'error': 'User is not a learner'}, status=status.HTTP_403_FORBIDDEN)

    # Get the session ID and description from the request
    session_id = request.data.get('session_id')
    description = request.data.get('description')

    # Check if the session exists and belongs to the learner
    try:
        session = Session.objects.get(id=session_id, learner=learner)
    except Session.DoesNotExist:
        return Response({'error': 'Session not found or does not belong to the learner'}, status=status.HTTP_404_NOT_FOUND)

    # Ensure the session is completed before adding a review
    if session.session_status != 'completed':
        return Response({'error': 'Cannot review a session that is not completed'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the educator from the session
    educator = session.educator

    # Create the review
    review = Review.objects.create(
        desc=description,
        learner=learner,
        educator=educator,
        session=session
    )

    # Serialize the review
    review_serializer = ReviewSerializer(review)
    return Response(review_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def scheduled_sessions(request):
    user = request.user
    
    # Ensure the request is made by an educator
    try:
        educator = Educator.objects.get(user=user)
    except Educator.DoesNotExist:
        return JsonResponse({'error': 'Only educators can view their scheduled sessions'}, status=status.HTTP_403_FORBIDDEN)
    
    # Fetch sessions with 'scheduled' status for the educator
    scheduled_sessions = Session.objects.filter(educator=educator, session_status='scheduled')
    
    # Serialize the sessions data
    session_serializer = SessionSerializer(scheduled_sessions, many=True)
    
    return JsonResponse({'scheduled_sessions': session_serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def session_history(request):
    user = request.user
    
    # Try to get the learner object for the user
    try:
        learner = Learner.objects.get(user=user)
    except Learner.DoesNotExist:
        learner = None
    
    # Try to get the educator object for the user
    try:
        educator = Educator.objects.get(user=user)
    except Educator.DoesNotExist:
        educator = None
    
    if learner:
        # If the user is a learner, get their completed sessions
        completed_sessions = Session.objects.filter(learner=learner, session_status='completed')
    elif educator:
        # If the user is an educator, get their completed sessions
        completed_sessions = Session.objects.filter(educator=educator, session_status='completed')
    else:
        # If the user is neither a learner nor an educator
        return JsonResponse({'error': 'User is neither a learner nor an educator'}, status=status.HTTP_403_FORBIDDEN)
    
    # Serialize the sessions data
    session_serializer = SessionSerializer(completed_sessions, many=True)
    
    return Response({'completed_sessions': session_serializer.data}, status=status.HTTP_200_OK)
