import React, {useState} from 'react';
import { useNavigate } from "react-router-dom"
import {Row, Col, Container} from "react-bootstrap"
import {Formik, Form, Field, ErrorMessage, FormikHelpers} from "formik"
import * as Yup from "yup"
import axios from 'axios';

function Signup() {

    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState("")

    const initialValues = {
        user_type:'buyer',
        buyer_name: "",
        buyer_username: "",
        buyer_email: "",
        buyer_password: "",
        confirm_password: ""
    }

    const validationSchema = Yup.object({
        buyer_username: Yup.string().required("Username is required"),
        buyer_name: Yup.string().required("Name is required"),
        buyer_email: Yup.string().required("Email is required").matches(/^[^@]+@[^@]+\.[^@]+$/, "Invalid email format"), 
        buyer_password: Yup.string().required("Password is required"),
        confirmPassword: Yup.string()
            .oneOf([Yup.ref('buyer_password')], "Passwords must match")
            .required("Passwords must match"),
    })

    const handleSubmit = async (values: any, { setSubmitting }: FormikHelpers<any>) => {
        setSubmitting(true)

        try {
            const response = await axios.post('/api/buyer_signup', values)
            console.log(response)

            if (response.status === 201) {
                const token = response.data.token
                localStorage.setItem('auth_token', token)
            }

            setErrorMessage('')
            navigate("/")
        } catch (error) {
            console.error(error)
            setErrorMessage('Signup failed. Please try again')
        } finally {
            setSubmitting(false)
        }

    }

    return (
        
        <Container>
            <Row>
                <Formik
                    initialValues={initialValues}
                    validationSchema={validationSchema}
                    onSubmit={handleSubmit}
                >
                    <Form className="signup-form">
                        <h3>Sign up</h3>
                        {errorMessage && (
                            <div className="error-message">{errorMessage}</div>
                        )}
                        <div className="form-group">
                            <label htmlFor="buyer_name">Name:</label>
                            <Field type="text" name="buyer_name" id="buyer_name" className="form-control form-field" />
                            <ErrorMessage name="buyer_name" component="div" className="error-message" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="buyer_email">Email:</label>
                            <Field type="text" name="buyer_email" id="buyer_email" className="form-control form-field" />
                            <ErrorMessage name="buyer_email" component="div" className="error-message" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="buyer_username">Username:</label>
                            <Field type="text" name="buyer_username" id="buyer_username" className="form-control form-field" />
                            <ErrorMessage name="buyer_username" component="div" className="error-message" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="buyer_password">Password:</label>
                            <Field type="text" name="buyer_password" id="buyer_password" className="form-control form-field" />
                            <ErrorMessage name="buyer_password" component="div" className="error-message" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="confirmPassword">Confirm Password:</label>
                            <Field type="text" name="confirmPassword" id="confirmPassword" className="form-control form-field" />
                            <ErrorMessage name="confirmPassword" component="div" className="error-message" />
                        </div>
                        <button type="submit" className="signup-button">Submit</button>
                    </Form>
                </Formik>
                <p> Already a user?
                    <span 
                    style={{cursor: "pointer"}}
                    onClick={() => navigate("/login")}>
                        <b> Login</b>
                    </span>
                </p>
            </Row>
        </Container>
        
    );
}

export default Signup;