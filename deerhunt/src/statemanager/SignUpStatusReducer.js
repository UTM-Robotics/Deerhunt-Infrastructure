export const initialState = {
    userSignStatus: 'null',
};

const SignUpReducer = (state,action) => {
    switch (action.type) {
        case 'SIGNED_UP':
            
            return {
                userSignStatus: 'success'
            }
        case 'SignUpFail':
            
            return {
                userSignStatus: 'fail'
            }
    
        default:
            return state;

}
};

export default SignUpReducer

