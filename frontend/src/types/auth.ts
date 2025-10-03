type LoginFormValues = {
    email: string;
    password: string;
};

type LoginFieldErrors = {
    [K in keyof LoginFormValues]?: string[];
};

export type LoginState = {
    success: boolean;
    error: {
        formErrors: string[];
        fieldErrors: LoginFieldErrors;
    } | null;
};

export type LogoutState = {
    success: boolean;
    error?: string;
};

type SignUpFormValues = {
    firstName: string;
    lastName: string;
    email: string;
    password: string;
};

type SignUpFieldErrors = {
    [K in keyof SignUpFormValues]?: string[];
};

export type SignUpState = {
    success?: boolean;
    error?: {
        formErrors: string[];
        fieldErrors: SignUpFieldErrors;
    };
};