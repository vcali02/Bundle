import React, {useState} from 'react';
import { useNavigate } from "react-router-dom"
import {Row, Col, Container} from "react-bootstrap"
import {Formik, Form, Field, ErrorMessage, FormikHelpers} from "formik"
import * as Yup from "yup"
import axios from 'axios'

function Login() {

    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState("")

    const initialValues = {
        user_type:'buyer',
        buyer_email: "",
        buyer_password: ""
    }

    const validationSchema = Yup.object({
        buyer_email: Yup.string().required("Email is required").matches(/^[^@]+@[^@]+\.[^@]+$/, "Invalid email format"), 
        buyer_password: Yup.string().required("Password is required"),
    })

    const handleSubmit = async (values: any, { setSubmitting }: FormikHelpers<any>) => {
        setSubmitting(true)

        try {
            const response = await axios.post('/api/buyer_login', values)
            console.log(response)

            if (response.status === 200) {
                const token = response.data.token
                localStorage.setItem('auth_token', token)
            }

            setErrorMessage('')
            navigate("/")
        } catch (error) {
            console.error(error)
            setErrorMessage('Login failed. Please try again')
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
                        <h3>Login</h3>
                        {errorMessage && (
                            <div className="error-message">{errorMessage}</div>
                        )}
                        <div className="form-group">
                            <label htmlFor="buyer_email">Email:</label>
                            <Field type="text" name="buyer_email" id="buyer_email" className="form-control form-field" />
                            <ErrorMessage name="buyer_email" component="div" className="error-message" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="buyer_password">Password:</label>
                            <Field type="text" name="buyer_password" id="buyer_password" className="form-control form-field" />
                            <ErrorMessage name="buyer_password" component="div" className="error-message" />
                        </div>
                        <button type="submit" className="signup-button">Submit</button>
                    </Form>
                </Formik>
                <p> Dont have an account?
                    <span 
                    style={{cursor: "pointer"}}
                    onClick={() => navigate("/signup")}>
                        <b> Sign up</b>
                    </span>
                </p>
            </Row>
        </Container>
    );
}

export default Login;