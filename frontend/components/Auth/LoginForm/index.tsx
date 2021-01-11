import React, { memo } from "react";
import { Wrapper } from "./styles";
import { Formik, Form, FormikProps } from "formik";
import { SButton } from "@/components/UI/Button";
import { Input } from "@/components/UI/Input";
import { object, string } from "yup";

const validationSchema = object().shape({
  email: string().email("Некорректный E-mail").required("Введите E-mail"),
  password: string().required("Введите пароль"),
});

export interface LoginFormValues {
  email: string;
  password: string;
}

interface LoginFormProps {
  handleSubmit: (values: LoginFormValues) => void;
}

const LoginFormComponent: React.FC<LoginFormProps> = ({ handleSubmit }) => {
  return (
    <Wrapper>
      <Formik
        initialValues={{
          email: "",
          password: "",
        }}
        validationSchema={validationSchema}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          setSubmitting(true);
          handleSubmit(values);
          setSubmitting(false);
          resetForm();
        }}
      >
        {(props: FormikProps<LoginFormValues>) => (
          <Form>
            <Input type="text" name="email" placeholder="E-mail" src="email" />
            <Input
              type="password"
              name="password"
              placeholder="Пароль"
              src="padlock"
            />
            <SButton myType="white" type="submit">
              Продолжить
            </SButton>
          </Form>
        )}
      </Formik>
    </Wrapper>
  );
};

export const LoginForm = memo(LoginFormComponent);
