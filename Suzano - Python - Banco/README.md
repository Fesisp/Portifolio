# Bank Account Management System

A robust banking system implementation in Python that demonstrates object-oriented programming principles, clean code practices, and software design patterns. Available both as a command-line application and a web interface.

## Live Demo

Try the interactive web version: [FesisBank Web Demo](#) *(Adicione o link quando hospedar)*

## Features

- **Account Management**
  - Create and manage multiple bank accounts
  - Support for different account types (extensible architecture)
  - Transaction history tracking
  
- **Client Management**
  - Create and manage client profiles
  - Support for individual customers (PessoaFisica)
  - Multiple accounts per client
  
- **Transaction Processing**
  - Deposits
  - Withdrawals with daily limits
  - Transaction history and statements
  
- **Security Features**
  - Input validation
  - Transaction limits
  - Daily withdrawal limits

## Technical Highlights

- **Clean Architecture**
  - Follows SOLID principles
  - Uses abstract classes and inheritance
  - Implements design patterns

- **Object-Oriented Design**
  - Abstract base classes for extensibility
  - Clear separation of concerns
  - Modular component design

## Installation and Deployment

### Local Development

```bash
# Clone the repository
git clone https://github.com/Fesisp/Portifolio.git

# Navigate to the project directory
cd "Suzano - Python - Banco"

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install required packages
pip install -r requirements.txt

# Run the command-line version
python bank_account.py

# Run the web version locally
streamlit run app_web.py
```

### Deployment Options

#### Option 1: Streamlit Cloud (Recommended)

1. Prepare your repository:
   - Ensure your code is in a public GitHub repository
   - Main file should be named `app_web.py`
   - Have a `requirements.txt` file

2. Deploy on Streamlit Cloud:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch, and `app_web.py`
   - Click "Deploy"

3. Access your app:
   - Streamlit will provide a public URL
   - Format: `https://your-app-name.streamlit.app`

#### Option 2: Self-Hosting (Railway)

1. Prepare for deployment:
   ```bash
   # Create Procfile
   echo "web: streamlit run app_web.py" > Procfile
   
   # Create runtime.txt
   echo "python-3.9.x" > runtime.txt
   ```

2. Deploy on Railway:
   - Create account on [Railway.app](https://railway.app)
   - Connect your GitHub repository
   - Create new project from GitHub
   - Select your repository
   - Add Python template
   - Set environment variables if needed
   - Deploy

3. Access your app:
   - Railway will provide a public URL
   - Configure custom domain if desired

## Usage Example

```python
# Create a new client
1. Select option [1] in main menu
2. Enter client details (CPF, name, birth date, address)

# Create a new account
1. Select option [2] in main menu
2. Enter client CPF
3. Account will be created automatically

# Perform transactions
1. Select option [4] to access account
2. Enter client CPF
3. Choose the account if multiple exist
4. Select desired operation (deposit/withdraw)
```

## Project Structure

```
Bank Account.py      # Main application file
README.md           # Project documentation
```

## Design Patterns Used

- **Abstract Factory**: For account creation
- **Command**: For transaction processing
- **Observer**: For transaction history

## Future Enhancements

- Implementation of additional account types
- Enhanced security features
- Database integration
- API implementation
- Unit test coverage

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
