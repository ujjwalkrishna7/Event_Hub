class PostForm(FlaskForm):
    title = StringField('Event', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')