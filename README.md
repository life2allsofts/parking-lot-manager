# Parking Management System with EV Charging Extension

A comprehensive parking management system demonstrating professional software architecture, domain-driven design, and enterprise-grade patterns. Originally a legacy codebase with significant anti-patterns, now transformed into a modern, scalable application.

## 🚀 Features

- **Multi-level Parking Management** - Support for regular and EV parking slots
- **Electric Vehicle Integration** - Smart charging station management
- **Professional GUI** - Tkinter-based interface with enhanced user experience
- **Layered Architecture** - Clear separation of GUI, business logic, and data layers
- **Domain-Driven Design** - Strategic bounded contexts and ubiquitous language
- **Comprehensive Testing** - Evidence-based validation across all development phases

## 🏗️ Architecture

Source_Code/
├── main.py                 # Application entry point
├── ParkingLot.py           # GUI layer and user interface
├── ParkingService.py       # Business logic layer
├── config.py              # Configuration management
└── models/
    ├── Vehicle.py         # Base vehicle class hierarchy
    └── ElectricVehicle.py # EV-specific functionality

## 📋 Requirements

- Python 3.6+
- No external dependencies - uses only standard library

## 🎯 Quick Start

1. Clone the repository:
bash
git clone https://github.com/life2allsofts/parking-lot-manager.git

2. Navigate to the source code:
bash
cd parking-management-system/Source_Code

3. Run the application:

python main.py

## 🎮 Usage

1. **Create Parking Lot**: Specify regular and EV slots for different levels
2. **Park Vehicles**: Support for cars, motorcycles, and electric vehicles
3. **Manage Operations**: Remove vehicles, check status, search by criteria
4. **Real-time Status**: Professional display of current occupancy

## 📊 Development Journey

### Phase 1: Anti-pattern Identification
- God Class elimination
- Inheritance hierarchy fixes
- Input validation implementation

### Phase 2: Critical Bug Fixes
- ElectricVehicle inheritance resolution
- Error handling and user experience improvements

### Phase 3: Architectural Refactoring
- Business logic separation
- Professional package structure
- Enhanced GUI with professional messaging

### Phase 4: Enterprise Patterns
- Domain-Driven Design analysis
- Microservices architecture specification
- UML documentation and design patterns

## 🗂️ Project Structure

parking-management-system/
├── Source_Code/                    # Complete working application
├── UML_Diagrams/                   # 7 structural and behavioral diagrams
├── Development_Screenshots/        # Development evidence across all phases
├── Application_Demonstration/      # Working application screenshots
├── Project_Documentation_DDD_and_Architecture.pdf
├── Project_Analysis_and_Refactoring.md
└── README.md

## 📈 Key Achievements

- **Eliminated God Class** from 817 to ~300 lines
- **Fixed Inheritance Hierarchy** for proper OOP
- **Implemented Layered Architecture** for maintainability
- **Designed Microservices-ready** structure
- **Applied Domain-Driven Design** principles
- **Professional UI/UX** with scrollable console and window management

## 🔧 Technical Highlights

- **SOLID Principles** implementation
- **Separation of Concerns** achieved
- **Professional Error Handling**
- **Comprehensive Input Validation**
- **Scalable Architecture** patterns
- **Domain-Driven Design** with bounded contexts

## 📝 Documentation

- **7 UML Diagrams** (structural and behavioral)
- **Domain-Driven Design** analysis with bounded contexts
- **Microservices Architecture** specification
- **Comprehensive Development** evidence
- **Professional UI/UX** refinement documentation

## 🎓 Academic Context

This project was developed as part of the **Quantic School of Business & Technology MSSE Program** for the **Software Design and Architecture Concentration**, demonstrating systematic refactoring from legacy code to professional architecture.

## 👥 Author

**Isaac Tetteh-Apotey**  
Geomatics Engineer | Quantic MSSE Student | AI-Driven Developer  
LinkedIn: https://www.linkedin.com/in/isaac-tetteh-apotey-67408b89/

## 📄 License

This project is for educational and portfolio purposes.

*Part of Quantic School of Business & Technology MSSE Program - Demonstrating software engineering excellence through systematic refactoring and professional architecture.*
