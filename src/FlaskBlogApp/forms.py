import email
from xmlrpc.client import Boolean
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from FlaskBlogApp.models import User



def maxImageSize(max_size=2):
    max_bytes = max_size * 1024 * 1024#Metatrepoume ta 2mb se bytes epeidi mporei na diavasei mono bytes h forma(1mb = 1024 kb= 1024 *1024bytees)
    def _check_file_size(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f'Το μέγεθος της εικόνας δεν μπορεί να υπερβαίνει τα {max_size} MB')
    
    return _check_file_size


def validate_email(form, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError("Αυτό το email υπάρχει ήδη")


class SignupForm(FlaskForm):
    username = StringField(label="Username", 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι απο 3 έως 15 χαρακτήρες")])
    
    email = StringField(label="email", 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Email(message="Παρακαλώ εισάγεται ένα σωστό email"), validate_email])
    
    password = StringField(label="password", 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι απο 3 έως 15 χαρακτήρες")])
    
    password2 = StringField(label="Επιβεβαίωση password", 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι απο 3 έως 15 χαρακτήρες"),
                            EqualTo('password', message="Τα δύο πεδία password πρέπει να είναι ίδια")])
    
    submit = SubmitField('Εγγραφή')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError("Αυτό το username υπάρχει ήδη")


class LoginForm(FlaskForm):
    
    email = StringField(label="email", 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Email(message="Παρακαλώ εισάγεται ένα σωστό email")])
    
    password = StringField(label="password", 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό.")])
    remember_me = BooleanField(label="Remember me")

    submit = SubmitField('Είσοδος')


class NewArticleForm(FlaskForm):
    
    article_title = StringField(label="Τίτλος", 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι απο 3 έως 50 χαρακτήρες")])
    
    article_body = TextAreaField(label="Κείμενο Άρθρου", 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Length(min=3, message="Το κείμενο του πεδίου πρέπει να έχει τουλάχιστον 5 χαρακτήρες")])

    article_image = FileField('Εικόνα Άρθρου', validators=[Optional(strip_whitespace=True),
                                                            FileAllowed([ 'jpg', 'jpeg', 'png' ], 'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, jpeg, png'),
                                                            maxImageSize(max_size=2)])


    submit = SubmitField('Αποστολή')



class AccountUpdateForm(FlaskForm):
    username = StringField(label="Username", 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι απο 3 έως 15 χαρακτήρες")])
    
    email = StringField(label="email", 
                            validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Email(message="Παρακαλώ εισάγεται ένα σωστό email")])
    
    profile_image = FileField('Εικόνα Προφίλ', validators=[Optional(strip_whitespace=True),
                                                            FileAllowed([ 'jpg', 'jpeg', 'png' ], 'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, jpeg, png'),
                                                            maxImageSize(max_size=2)])

    
    submit = SubmitField('Αποστολή')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Αυτό το username υπάρχει ήδη")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError("Αυτό το email υπάρχει ήδη")

