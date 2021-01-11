import { useField } from "formik";
import React, { memo, TextareaHTMLAttributes } from "react";
import { STextArea, STextAreaTag, STextAreaError } from "./styles";

type InputProps = TextareaHTMLAttributes<HTMLTextAreaElement> & {
  name: string;
  width?: string;
};

const TextAreaComponent: React.FC<InputProps> = (props) => {
  const [field, meta] = useField(props);
  const isShowError = meta.touched && !!meta.error;
  return (
    <STextArea>
      <STextAreaTag {...field} {...props} isShowError={isShowError} />
      {isShowError && <STextAreaError>{meta.error}</STextAreaError>}
    </STextArea>
  );
};

export const TextArea = memo(TextAreaComponent);
