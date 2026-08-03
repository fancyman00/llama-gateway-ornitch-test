# Clean Architecture structure

The gateway uses classic Clean Architecture with four layers: domain (entities, value objects, domain exceptions), application (use cases, interfaces, DTOs), infrastructure (adapters for database, Redis, HTTP clients), and presentation (FastAPI routes, request/response models). This separation enables clear testing boundaries and easy extension.
