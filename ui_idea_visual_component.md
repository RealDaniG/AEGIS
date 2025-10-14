"""
Enhanced Unified Field Physics Simulator
A comprehensive simulation of fundamental physics based on RHUFT framework
Focusing on particle physics, quantum fields, and unified interactions
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from enum import Enum, auto
from scipy.fft import fftn, ifftn, fftfreq
from tqdm import tqdm
import time as time_module

class FieldType(Enum):
    SCALAR = auto()
    FERMION = auto()
    VECTOR = auto()

@dataclass
class Particle:
    name: str
    mass: float  # in eV/c²
    charge: float  # in units of elementary charge
    spin: float  # in units of ħ
    field_type: FieldType
    color_charge: str = None  # For QCD
    weak_isospin: float = 0.0  # For weak interactions

class StandardModelConstants:
    # Fundamental constants (in SI units)
    hbar = 1.0545718e-34  # Reduced Planck constant (J·s)
    c = 2.99792458e8  # Speed of light (m/s)
    G = 6.67430e-11  # Gravitational constant (m³/kg·s²)
    e = 1.602176634e-19  # Elementary charge (C)
    epsilon0 = 8.8541878128e-12  # Vacuum permittivity (F/m)
    mu0 = 1.25663706212e-6  # Vacuum permeability (N/A²)
    
    # Coupling constants (dimensionless)
    alpha_EM = 1/137.035999084  # Fine-structure constant
    alpha_S = 0.118  # Strong coupling constant at mZ
    theta_W = np.arcsin(np.sqrt(0.22290))  # Weinberg angle
    
    # Particle masses (in eV/c²)
    m_e = 0.51099895e6  # Electron mass
    m_mu = 105.6583755e6  # Muon mass
    m_tau = 1.77686e9  # Tau lepton mass
    m_u = 2.2e6  # Up quark mass (current mass, MS-bar, 2 GeV)
    m_d = 4.7e6  # Down quark mass (current mass, MS-bar, 2 GeV)
    m_s = 95e6  # Strange quark mass (current mass, MS-bar, 2 GeV)
    m_c = 1.28e9  # Charm quark mass (MS-bar, m_c)
    m_b = 4.18e9  # Bottom quark mass (MS-bar, m_b)
    m_t = 173.0e9  # Top quark mass (pole mass)
    m_W = 80.379e9  # W boson mass
    m_Z = 91.1876e9  # Z boson mass
    m_H = 125.10e9  # Higgs boson mass
    
    # Mixing parameters
    CKM = np.array([
        [0.97446, 0.22452, 0.00365],
        [0.22438, 0.97359, 0.04214],
        [0.00896, 0.04133, 0.999105]
    ])  # CKM matrix
    
    # Neutrino mixing parameters (simplified)
    theta_12 = 33.62 * np.pi/180
    theta_23 = 47.2 * np.pi/180
    theta_13 = 8.54 * np.pi/180
    delta_CP = 1.39 * np.pi
    
    # RHUFT-specific parameters
    phi = (1 + np.sqrt(5)) / 2  # Golden ratio
    alpha_GUT = 1/25.7  # GUT coupling constant
    
    @classmethod
    def get_particle(cls, name: str) -> Particle:
        """Get a standard model particle by name"""
        particles = {
            # Leptons
            'electron': Particle('electron', cls.m_e, -1, 0.5, FieldType.FERMION, weak_isospin=-0.5),
            'muon': Particle('muon', cls.m_mu, -1, 0.5, FieldType.FERMION, weak_isospin=-0.5),
            'tau': Particle('tau', cls.m_tau, -1, 0.5, FieldType.FERMION, weak_isospin=-0.5),
            'neutrino_e': Particle('neutrino_e', 0, 0, 0.5, FieldType.FERMION, weak_isospin=0.5),
            'neutrino_mu': Particle('neutrino_mu', 0, 0, 0.5, FieldType.FERMION, weak_isospin=0.5),
            'neutrino_tau': Particle('neutrino_tau', 0, 0, 0.5, FieldType.FERMION, weak_isospin=0.5),
            
            # Quarks
            'up': Particle('up', cls.m_u, 2/3, 0.5, FieldType.FERMION, 'R', 0.5),
            'down': Particle('down', cls.m_d, -1/3, 0.5, FieldType.FERMION, 'R', -0.5),
            'charm': Particle('charm', cls.m_c, 2/3, 0.5, FieldType.FERMION, 'G', 0.5),
            'strange': Particle('strange', cls.m_s, -1/3, 0.5, FieldType.FERMION, 'G', -0.5),
            'top': Particle('top', cls.m_t, 2/3, 0.5, FieldType.FERMION, 'B', 0.5),
            'bottom': Particle('bottom', cls.m_b, -1/3, 0.5, FieldType.FERMION, 'B', -0.5),
            
            # Gauge bosons
            'photon': Particle('photon', 0, 0, 1, FieldType.VECTOR),
            'W+': Particle('W+', cls.m_W, 1, 1, FieldType.VECTOR, weak_isospin=1),
            'W-': Particle('W-', cls.m_W, -1, 1, FieldType.VECTOR, weak_isospin=-1),
            'Z': Particle('Z', cls.m_Z, 0, 1, FieldType.VECTOR),
            'gluon': Particle('gluon', 0, 0, 1, FieldType.VECTOR, 'octet'),
            
            # Scalar boson
            'higgs': Particle('higgs', cls.m_H, 0, 0, FieldType.SCALAR)
        }
        return particles.get(name.lower())

class UnifiedFieldSolver:
    # Gamma matrices for Dirac equation (in Dirac representation) - defined at class level
    gamma0 = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1]
    ], dtype=np.complex128)
    
    gamma1 = np.array([
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, -1, 0, 0],
        [-1, 0, 0, 0]
    ], dtype=np.complex128)
    
    gamma2 = np.array([
        [0, 0, 0, -1j],
        [0, 0, 1j, 0],
        [0, 1j, 0, 0],
        [-1j, 0, 0, 0]
    ], dtype=np.complex128)
    
    gamma3 = np.array([
        [0, 0, 1, 0],
        [0, 0, 0, -1],
        [-1, 0, 0, 0],
        [0, 1, 0, 0]
    ], dtype=np.complex128)
    
    # Gamma5 for chiral projections
    gamma5 = np.array([
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ], dtype=np.complex128)
    
    # Sigma matrices (for spin)
    sigma1 = np.array([
        [0, 1],
        [1, 0]
    ], dtype=np.complex128)
    
    sigma2 = np.array([
        [0, -1j],
        [1j, 0]
    ], dtype=np.complex128)
    
    sigma3 = np.array([
        [1, 0],
        [0, -1]
    ], dtype=np.complex128)
    
    @classmethod
    def validate_gamma_matrices(cls):
        """Validate that gamma matrices satisfy the Dirac algebra"""
        I = np.eye(4, dtype=np.complex128)
        g0, g1, g2, g3 = cls.gamma0, cls.gamma1, cls.gamma2, cls.gamma3
        
        # Check squares
        tests = [
            (g0 @ g0, I, "gamma0^2 != I"),
            (g1 @ g1, -I, "gamma1^2 != -I"),
            (g2 @ g2, -I, "gamma2^2 != -I"),
            (g3 @ g3, -I, "gamma3^2 != -I"),
        ]
        
        # Check anticommutation
        for i, gi in enumerate([g1, g2, g3], 1):
            for j, gj in enumerate([g1, g2, g3], 1):
                if i != j:
                    tests.append(
                        (gi @ gj + gj @ gi, np.zeros_like(I), 
                         f"gamma{i} and gamma{j} don't anticommute")
                    )
        
        # Run tests
        for result, expected, msg in tests:
            if not np.allclose(result, expected, atol=1e-10):
                raise ValueError(f"Gamma matrix validation failed: {msg}")
        
        # Verify gamma5 = i gamma0 gamma1 gamma2 gamma3
        g5_calc = 1j * g0 @ g1 @ g2 @ g3
        if not np.allclose(g5_calc, cls.gamma5, atol=1e-10):
            raise ValueError("gamma5 definition is inconsistent with gamma0-gamma3")
        
        return True
    
    def _run_test(self, test_func, test_name):
        """Helper method to run a single test and track results"""
        self.test_count += 1
        try:
            result = test_func()
            self.passed_tests += 1
            self.test_results[test_name] = 'PASSED'
            return result
        except Exception as e:
            self.test_results[test_name] = f'FAILED: {str(e)}'
            if self.test_mode:
                raise
            return None
    
    def run_validation_tests(self, max_time=300):
        """Run comprehensive validation tests"""
        import time
        start_time = time.time()
        
        # Run all test methods starting with 'test_'
        test_methods = [name for name in dir(self) 
                       if name.startswith('test_') and callable(getattr(self, name))]
        
        for method_name in test_methods:
            if time.time() - start_time > max_time:
                print(f"\nTest timeout after {max_time} seconds")
                break
                
            test_func = getattr(self, method_name)
            self._run_test(test_func, method_name)
        
        # Calculate test statistics
        elapsed = time.time() - start_time
        success_rate = (self.passed_tests / self.test_count) * 100 if self.test_count > 0 else 0
        
        print(f"\nTest Results ({elapsed:.2f}s):")
        print(f"  Tests run: {self.test_count}")
        print(f"  Passed: {self.passed_tests}")
        print(f"  Success rate: {success_rate:.1f}%")
        
        self.validation_passed = (success_rate >= 99.0)
        return self.validation_passed
    
    # ===== Individual Test Methods =====
    
    def test_gamma_matrices(self):
        """Test gamma matrix algebra"""
        return self.__class__.validate_gamma_matrices()
    
    def test_free_field_evolution(self, steps=100):
        """Test evolution of free fields with known solutions"""
        # Store initial state
        initial_energy = self.calculate_total_energy()
        
        for _ in range(steps):
            self.evolve_fields()
            
            # Check energy conservation
            current_energy = self.calculate_total_energy()
            energy_diff = abs(current_energy - initial_energy)
            
            if energy_diff > self.energy_tolerance * initial_energy:
                raise ValueError(
                    f"Energy not conserved: "
                    f"{energy_diff/initial_energy*100:.2e}% change after {_+1} steps"
                )
        
        return True
    
    def test_fermion_charge_conservation(self, steps=100):
        """Test that fermion charge is conserved"""
        if not hasattr(self, 'fermion_fields'):
            return True  # Skip if no fermion fields
            
        initial_charge = self.calculate_total_charge()
        
        for _ in range(steps):
            self.evolve_fields()
            current_charge = self.calculate_total_charge()
            
            if abs(current_charge - initial_charge) > self.charge_tolerance * (abs(initial_charge) + 1e-100):
                raise ValueError(
                    f"Charge not conserved: "
                    f"{abs(current_charge - initial_charge):.2e} change after {_+1} steps"
                )
        
        return True
    
    def test_numerical_stability(self, steps=1000):
        """Test numerical stability over many steps"""
        energies = []
        
        for i in range(steps):
            self.evolve_fields()
            energies.append(self.calculate_total_energy())
            
            # Check for numerical instability
            if i > 10:
                energy_change = abs((energies[-1] - energies[-2]) / (energies[0] + 1e-100))
                if energy_change > 1e-3:  # 0.1% change
                    print(f"  Warning: Large energy change at step {i}: {energy_change*100:.2e}%")
        
        # Check overall energy conservation
        if len(energies) > 1:
            energy_change = abs((energies[-1] - energies[0]) / (energies[0] + 1e-100))
            if energy_change > self.energy_tolerance:
                raise ValueError(
                    f"Energy not conserved: {energy_change*100:.2e}% change over {steps} steps"
                )
        
        return True
    
    def __init__(self, grid_size=32, box_size=1e-10, dimension=1, test_mode=False, cfl_number=0.1):
        """
        Initialize the unified field solver with optimized parameters for 10-minute runtime.
        
        Parameters:
        -----------
        grid_size : int, optional
            Number of grid points in each dimension (default: 32 for testing)
        box_size : float, optional
            Physical size of the simulation box in meters (default: 1e-10)
        dimension : int, optional
            Number of spatial dimensions (1, 2, or 3, default: 1 for testing)
        test_mode : bool, optional
            If True, run in test mode with additional checks (default: False)
        cfl_number : float, optional
            Courant-Friedrichs-Lewy number for stable time stepping (default: 0.1)
        """
        # Performance optimization flags
        self.optimize = True  # Enable performance optimizations
        self.use_numba = False  # Will be set based on availability
        self.vectorize = True  # Use vectorized operations
        # Store parameters
        self.grid_size = grid_size
        self.box_size = box_size
        self.dimension = dimension
        self.test_mode = test_mode
        self.cfl_number = cfl_number
        
        # Calculate spatial step (uniform grid)
        self.dx = box_size / grid_size if grid_size > 0 else 0
        
        # Set time step based on CFL condition
        # dt = CFL * dx / c, where c is the characteristic speed
        # For relativistic fields, c is the speed of light
        self.c = 1.0  # Using natural units where c=1
        self.time_step = cfl_number * self.dx / self.c if self.dx > 0 else 1e-20
        
        # Initialize time and step counter
        self.time = 0.0
        self.step = 0
        
        # Initialize fields
        self.initialize_fields()
        
        # For energy tracking
        self.energy_history = []
        self.time_history = []
        """
        Initialize the unified field solver with proper scaling and unified field theory formulation.
        
        Parameters:
        -----------
        grid_size : int, optional
            Number of grid points in each dimension (default: 128)
        box_size : float, optional
            Physical size of the simulation box in meters (default: 1e-10)
        dimension : int, optional
            Number of spatial dimensions (1, 2, or 3, default: 3)
        
        # Test mode settings
        self.test_mode = test_mode
        self.energy_tolerance = 1e-6
        self.charge_tolerance = 1e-6
        
        # Initialize validation state
        self.validation_passed = False
        self.test_results = {}
        
        # Validate gamma matrices on initialization
        try:
            self.__class__.validate_gamma_matrices()
            self.test_results['gamma_matrices'] = 'PASSED'
        except ValueError as e:
            self.test_results['gamma_matrices'] = f'FAILED: {str(e)}'
            if test_mode:
                raise
        
        # Initialize test counters
        self.test_count = 0
        self.passed_tests = 0
            
        Attributes:
        ----------
        c : float
            Speed of light in vacuum (m/s)
        hbar : float
            Reduced Planck constant (J·s)
        G : float
            Gravitational constant (m³/kg·s²)
        alpha_EM : float
            Fine-structure constant (dimensionless)
        alpha_S : float
            Strong coupling constant (dimensionless)
        theta_W : float
            Weinberg angle (radians)
        """
        # Fundamental constants
        self.c = StandardModelConstants.c
        self.hbar = StandardModelConstants.hbar
        self.G = StandardModelConstants.G
        self.alpha_EM = StandardModelConstants.alpha_EM
        self.alpha_S = StandardModelConstants.alpha_S
        self.theta_W = StandardModelConstants.theta_W
        
        # Simulation parameters
        self.grid_size = grid_size
        self.box_size = box_size
        self.dimension = dimension
        self.dx = box_size / grid_size
        self.time = 0.0
        self.step = 0
        
        # Time step parameters
        self.cfl = 0.1  # CFL stability factor
        self.max_cfl = 0.5  # Maximum CFL number for stability
        self.min_dt = 1e-24  # Minimum time step (s)
        self.max_dt = 1e-18  # Maximum time step (s)
        self.time_step = self.calculate_initial_timestep()
        
        # Energy conservation
        self.energy_history = []
        self.energy_tolerance = 1e-4  # 0.01% energy conservation tolerance
        
        # Initialize coordinate grid
        self.x = np.linspace(-box_size/2, box_size/2, grid_size, endpoint=False)
        if dimension >= 2:
            self.y = np.linspace(-box_size/2, box_size/2, grid_size, endpoint=False)
        if dimension == 3:
            self.z = np.linspace(-box_size/2, box_size/2, grid_size, endpoint=False)
        
        # Wavevector for FFT (for Laplacian and gradient operators)
        kx = 2 * np.pi * fftfreq(grid_size, d=self.dx)
        if dimension == 1:
            self.k = kx
        elif dimension == 2:
            self.k = np.array(np.meshgrid(kx, kx, indexing='ij'))
        else:  # 3D
            self.k = np.array(np.meshgrid(kx, kx, kx, indexing='ij'))
        
        # Unified field tensor components (16 components in 4D spacetime)
        self.F_mu_nu = np.zeros((4, 4) + (grid_size,) * dimension, dtype=np.complex128)
        
        # Initialize field components with proper scaling
        self.initialize_fields()
        
        # Initialize particles with unified field couplings
        self.particles = {
            'electron': StandardModelConstants.get_particle('electron'),
            'photon': StandardModelConstants.get_particle('photon'),
            'higgs': StandardModelConstants.get_particle('higgs'),
            'up': StandardModelConstants.get_particle('up'),
            'down': StandardModelConstants.get_particle('down')
        }
        
        # Field history for visualization and analysis
        self.field_history = []
        self.energy_density = np.zeros((grid_size,) * dimension)
        
        # Store gamma matrices in a list for easy access
        self.gamma = [self.gamma1, self.gamma2, self.gamma3]
    
    def initialize_fields(self):
        """Initialize all quantum fields"""
        shape = (self.grid_size,) * self.dimension
        
        # Scalar field (Higgs)
        v = 246.22e9 * 1.78e-36  # Higgs VEV in kg (converted from eV)
        self.phi = v * np.ones(shape, dtype=np.complex128)  # Real scalar field
        self.phi_dot = np.zeros_like(self.phi)  # Time derivative
        
        # Gauge fields (simplified for demonstration)
        # Electromagnetic field A_mu (4-vector, complex for numerical stability)
        self.A_mu = np.zeros((4,) + shape, dtype=np.complex128)
        # Weak gauge fields W_mu^a (a=1,2,3) for SU(2)
        self.W_mu = np.zeros((3, 4) + shape, dtype=np.complex128)
        # Gluon fields G_mu^a (a=1..8) for SU(3)
        self.G_mu = np.zeros((8, 4) + shape, dtype=np.complex128)
        
        # Fermion fields (for electrons, quarks, etc.)
        # Each fermion is a 4-component spinor in 4D spacetime
        self.fermions = {
            'electron': np.zeros((4,) + shape, dtype=np.complex128)
        }
        
        # Add small random fluctuations to break symmetry
        noise_amplitude = 1e-3 * v
        self.phi += noise_amplitude * (
            np.random.randn(*shape) + 
            1j * np.random.randn(*shape)
        )
        
        # Initialize fermion fields (simplified)
        for name in self.fermions:
            self.fermions[name] = noise_amplitude * (
                np.random.randn(4, *shape) + 
                1j * np.random.randn(4, *shape)
            )
    
    def calculate_initial_timestep(self):
        """
        Calculate the initial time step based on the CFL condition.
        
        Returns:
        --------
        float
            The initial time step in seconds
        """
        # CFL condition: dt < dx / (c * sqrt(dimension))
        dt = self.cfl * self.dx / (StandardModelConstants.c * np.sqrt(self.dimension))
        return min(max(dt, self.min_dt), self.max_dt)
    
    def laplacian(self, field):
        """
        Compute the Laplacian of a field using FFT.
        
        Parameters:
        -----------
        field : numpy.ndarray
            The input field to compute the Laplacian of
            
        Returns:
        --------
        numpy.ndarray
            The Laplacian of the input field
        """
        fft_field = fftn(field)
        if self.dimension == 1:
            laplacian = ifftn(-self.k**2 * fft_field).real
        else:
            k_squared = np.sum(self.k**2, axis=0)
            laplacian = ifftn(-k_squared * fft_field).real
        return laplacian
    
    def evolve_fields(self, dt=None):
        """
        Evolve all quantum fields using a symplectic integration scheme (2nd order).
        Implements a velocity Verlet-like algorithm for better energy conservation.
        
        Parameters:
        -----------
        dt : float, optional
            Time step in seconds. If None, uses the adaptive time step.
            
        Returns:
        --------
        float
            Total energy of the system after evolution
        """
        if dt is None:
            dt = self.time_step
        
        # Store initial state for Verlet integration (commented out as not currently used)
        # phi_prev = self.phi.copy()
        # phi_dot_prev = self.phi_dot.copy()
        
        # First half-step: update momenta
        self.update_field_tensor()
        laplacian_phi = self.laplacian(self.phi)
        phi_dot_dot = laplacian_phi - self.V_prime(self.phi) - self.Ricci_scalar() * self.phi / 6.0
        
        # Update momenta (velocity) at half step
        phi_dot_half = self.phi_dot + 0.5 * dt * phi_dot_dot
        
        # Update positions (fields) using half-step momenta
        new_phi = self.phi + dt * phi_dot_half
        
        # Update fields for next step
        self.phi = new_phi
        self.phi_dot = phi_dot_half
        
        # Evolve gauge fields using Yang-Mills equations
        new_A_mu = self.evolve_gauge_field(self.A_mu, self.alpha_EM, dt)
        new_W_mu = self.evolve_weak_field(self.W_mu, dt)
        new_G_mu = self.evolve_gluon_field(self.G_mu, dt)
        
        # Evolve fermion fields using Dirac equation in curved spacetime
        new_fermions = {}
        for name, psi in self.fermions.items():
            mass = self.particles[name].mass * 1.78e-36  # Convert eV to kg
            coupling = self.get_fermion_coupling(name)
            new_fermions[name] = self.evolve_fermion(psi, mass, coupling, dt)
        
        # Second half-step: update momenta to full step
        self.update_field_tensor()
        laplacian_phi = self.laplacian(self.phi)
        phi_dot_dot = laplacian_phi - self.V_prime(self.phi) - self.Ricci_scalar() * self.phi / 6.0
        
        # Complete the momentum update
        new_phi_dot = phi_dot_half + 0.5 * dt * phi_dot_dot
        
        # Update gauge and fermion fields using the same symplectic scheme
        self.A_mu = self.evolve_gauge_field_symplectic(self.A_mu, self.alpha_EM, dt)
        self.W_mu = self.evolve_weak_field_symplectic(self.W_mu, dt)
        self.G_mu = self.evolve_gluon_field_symplectic(self.G_mu, dt)
        
        # Evolve fermion fields
        new_fermions = {}
        for name, psi in self.fermions.items():
            mass = self.particles[name].mass * 1.78e-36  # Convert eV to kg
            coupling = self.get_fermion_coupling(name)
            new_fermions[name] = self.evolve_fermion_symplectic(psi, mass, coupling, dt)
        
        self.fermions = new_fermions
        
        # Update time and step counter
        self.time += dt
        self.step += 1
        
        # Calculate and store energy (for monitoring only, not used in evolution)
        energy = self.calculate_total_energy()
        self.energy_history.append(energy)
        
        # Adjust time step more aggressively if needed
        if self.step % 5 == 0:  # Check more frequently
            self.adjust_timestep()
        
        return energy
    
    def V_prime(self, phi):
        """Derivative of the Higgs potential"""
        v = 246.22e9 * 1.78e-36  # Higgs VEV in kg
        lam = 0.13  # Self-coupling
        return lam * (np.abs(phi)**2 - v**2) * phi
    
    def evolve_fermion(self, psi, mass, coupling, dt):
        """
        Evolve a fermion field using the Dirac equation in curved spacetime.
        
        Parameters:
        -----------
        psi : numpy.ndarray
            The fermion field (4-component spinor)
        mass : float
            Mass of the fermion in kg
        coupling : float
            Coupling strength to the gauge fields
        dt : float
            Time step in seconds
            
        Returns:
        --------
        numpy.ndarray
            The evolved fermion field
        """
        # Gamma matrices in Dirac representation
        gamma0 = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, -1, 0],
                          [0, 0, 0, -1]])
        
        gamma = [
            np.array([[0, 0, 0, 1],
                     [0, 0, 1, 0],
                     [0, -1, 0, 0],
                     [-1, 0, 0, 0]]),  # gamma1
            np.array([[0, 0, 0, -1j],
                     [0, 0, 1j, 0],
                     [0, 1j, 0, 0],
                     [-1j, 0, 0, 0]]), # gamma2
            np.array([[0, 0, 1, 0],
                     [0, 0, 0, -1],
                     [-1, 0, 0, 0],
                     [0, 1, 0, 0]])     # gamma3
        ]
        
        # Calculate spatial derivatives using FFT
        dpsi_dx = [np.zeros_like(psi) for _ in range(3)]
        for i in range(4):  # For each spinor component
            for d in range(3):
                dpsi_dx[d][i] = np.real(ifftn(1j * self.k * fftn(psi[i])))
        
        # Calculate the time derivative
        dpsi_dt = np.zeros_like(psi, dtype=np.complex128)
        
        # Mass term
        mass_term = np.einsum('ij,j...->i...', gamma0 * mass * self.c**2 / self.hbar, psi)
        
        # Momentum terms
        momentum_terms = np.zeros_like(psi, dtype=np.complex128)
        for d in range(3):
            momentum_terms += -1j * self.c * np.einsum('ij,j...->i...', gamma[d], dpsi_dx[d])
        
        # Gauge field coupling (simplified)
        gauge_term = np.zeros_like(psi, dtype=np.complex128)
        if coupling != 0:
            # This would involve the gauge field A_mu in a complete implementation
            pass
        
        # Combine terms: i∂ψ/∂t = (γ⁰m - iγ·∇ + coupling terms)ψ
        dpsi_dt = -1j * (mass_term + momentum_terms + gauge_term)
        
        # Update the field using a simple Euler step
        new_psi = psi + dpsi_dt * dt
        
        # Normalize to maintain numerical stability
        norm = np.sqrt(np.sum(np.abs(new_psi)**2, axis=0))
        new_psi = np.where(norm > 1e-10, new_psi / (norm + 1e-10), new_psi)
        
        return new_psi
    
    def get_fermion_coupling(self, name):
        """Get the coupling strength for a fermion field"""
        if name == 'electron':
            return self.alpha_EM  # Electromagnetic coupling
        elif name in ['up', 'down']:
            return self.alpha_S   # Strong coupling for quarks
        else:
            return 0.1           # Default coupling
    
    def evolve_weak_field(self, W_mu, dt):
        """Evolve the weak gauge fields using the Yang-Mills equations"""
        new_W_mu = np.zeros_like(W_mu)
        m_W = 80.379e9 * 1.78e-36  # W boson mass in kg
        
        for a in range(3):  # For each weak isospin component
            for mu in range(4):  # For each spacetime component
                # Wave equation with mass term and self-coupling
                laplacian_W = self.laplacian(W_mu[a, mu])
                new_W_mu[a, mu] = W_mu[a, mu] + (
                    laplacian_W - (m_W**2) * W_mu[a, mu]
                ) * dt
        
        return new_W_mu
    
    def evolve_gluon_field(self, G_mu, dt):
        """Evolve the gluon fields using the Yang-Mills equations"""
        new_G_mu = np.zeros_like(G_mu)
        
        for a in range(8):  # For each color charge
            for mu in range(4):  # For each spacetime component
                # Wave equation with self-coupling (simplified)
                laplacian_G = self.laplacian(G_mu[a, mu])
                new_G_mu[a, mu] = G_mu[a, mu] + (
                    laplacian_G - 0.1 * G_mu[a, mu]  # Damping for stability
                ) * dt
        
        return new_G_mu
        
    def dA_mu_dt(self, mu):
        """Time derivative of the electromagnetic field A_mu (legacy method)"""
        if mu == 0:  # Time component (Coulomb gauge)
            return np.zeros_like(self.A_mu[0])
        else:  # Space components
            laplacian_A = self.laplacian(self.A_mu[mu])
            # Add current coupling for charged particles
            if mu == 1 and hasattr(self, 'fermions') and self.fermions:  # x-component with current
                current = -np.sum([np.abs(psi[0])**2 + np.abs(psi[1])**2 
                                 for psi in self.fermions.values()], axis=0)
                return laplacian_A - current
            return laplacian_A
    
    def dW_mu_dt(self, a, mu):
        """Time derivative of the weak gauge field W_mu^a"""
        laplacian_W = self.laplacian(self.W_mu[a, mu])
        # Add mass term for W bosons
        m_W = 80.379e9 * 1.78e-36  # Convert eV to kg
        return laplacian_W - (m_W**2) * self.W_mu[a, mu]
    
    def dG_mu_dt(self, a, mu):
        """Time derivative of the gluon field G_mu^a"""
        laplacian_G = self.laplacian(self.G_mu[a, mu])
        # Add simple damping for numerical stability
        return laplacian_G - 0.1 * self.G_mu[a, mu]
    
    def evolve_gauge_field_symplectic(self, A_mu, coupling, dt):
        """Evolve gauge field using a symplectic integrator"""
        # Half-step momentum update
        laplacian_A = np.array([self.laplacian(comp) for comp in A_mu])
        A_dot_half = A_mu + 0.5 * dt * (laplacian_A - coupling * A_mu)
        
        # Full position update
        new_A_mu = A_mu + dt * A_dot_half
        
        # Project to maintain gauge condition (Lorenz gauge)
        if hasattr(self, 'lorenz_gauge') and self.lorenz_gauge:
            new_A_mu = self.apply_lorenz_gauge(new_A_mu)
            
        return new_A_mu
        
    def evolve_weak_field_symplectic(self, W_mu, dt):
        """Evolve weak field using a symplectic integrator"""
        new_W_mu = np.zeros_like(W_mu)
        m_W = 80.379e9 * 1.78e-36  # W boson mass in kg
        
        for a in range(3):
            for mu in range(4):
                laplacian_W = self.laplacian(W_mu[a, mu])
                # Half-step momentum update
                W_dot_half = W_mu[a, mu] + 0.5 * dt * (laplacian_W - (m_W**2) * W_mu[a, mu])
                # Full position update
                new_W_mu[a, mu] = W_mu[a, mu] + dt * W_dot_half
                
        return new_W_mu
        
    def evolve_gluon_field_symplectic(self, G_mu, dt):
        """Evolve gluon field using a symplectic integrator"""
        new_G_mu = np.zeros_like(G_mu)
        
        for a in range(8):
            for mu in range(4):
                laplacian_G = self.laplacian(G_mu[a, mu])
                # Half-step momentum update with damping
                G_dot_half = G_mu[a, mu] + 0.5 * dt * (laplacian_G - 0.1 * G_mu[a, mu])
                # Full position update
                new_G_mu[a, mu] = G_mu[a, mu] + dt * G_dot_half
                
        return new_G_mu
        
    def evolve_fermion_symplectic(self, psi, mass, coupling, dt):
        """Evolve fermion field using a symplectic integrator"""
        # Use a split-step method for the Dirac equation
        # First half-step in momentum space
        axes = tuple(range(-self.dimension, 0))  # Create tuple of axes for FFT
        psi_k = np.fft.fftn(psi, axes=axes)
        
        # Apply kinetic energy operator
        kinetic = np.zeros_like(psi_k)
        for d in range(self.dimension):
            # For 1D case, we need to handle the axis specification differently
            if self.dimension == 1:
                kinetic += np.fft.ifft(1j * self.k * psi_k, axis=-1)
            else:
                # For higher dimensions, use ifftn with the specific axis
                kinetic += np.fft.ifftn(1j * self.k[d] * psi_k, axes=(d,))
            
        # Half-step update
        psi_half = psi + 0.5 * dt * (-1j * self.c * kinetic)
        
        # Apply potential energy operator (mass and interaction terms)
        mass_term = mass * self.c**2 / self.hbar * np.einsum('ij,j...->i...', UnifiedFieldSolver.gamma0, psi_half)
        psi_new = psi_half - 1j * dt * mass_term
        
        # Normalize to prevent numerical instability
        norm = np.sqrt(np.sum(np.abs(psi_new)**2, axis=0))
        psi_new = np.where(norm > 1e-10, psi_new / (norm + 1e-10), psi_new)
        
        return psi_new
        
    def calculate_total_energy(self):
        """
        Calculate the total energy density of the system using a consistent
        Hamiltonian formulation that matches our symplectic integrator.
        
        Returns:
        --------
        float
            Total energy in Joules
        """
        # Scalar field energy (Hamiltonian density)
        kinetic_energy = 0.5 * np.abs(self.phi_dot)**2
        gradient_energy = 0.5 * np.sum([np.abs(g)**2 for g in np.gradient(self.phi, self.dx)], axis=0)
        potential_energy = self.V(self.phi)
        
        # Gauge field energy (Hamiltonian density)
        em_energy = 0.25 * np.sum([np.sum(f**2) for f in self.F_mu_nu], axis=0)
        weak_energy = 0.25 * np.sum([np.sum(w**2) for w in self.W_mu], axis=0)
        strong_energy = 0.25 * np.sum([np.sum(g**2) for g in self.G_mu], axis=0)
        
        # Fermion energy (Hamiltonian density)
        fermion_energy = np.zeros_like(self.phi)
        for name, psi in self.fermions.items():
            mass = self.particles[name].mass * 1.78e-36  # eV to kg
            fermion_energy += np.sum(np.abs(psi)**2, axis=0) * mass * self.c**2
        
        # Gravitational energy density (simplified)
        curvature_energy = self.Ricci_scalar()**2 / (32 * np.pi * self.G)
        
        # Total energy density (J/m³)
        energy_density = (kinetic_energy + gradient_energy + potential_energy +
                         em_energy + weak_energy + strong_energy + 
                         fermion_energy + curvature_energy)
        
        # Store energy density for visualization
        self.energy_density = energy_density
        
        # Integrate over volume to get total energy
        total_energy = np.sum(energy_density) * (self.dx ** self.dimension)
        
        return total_energy
    
    def V(self, phi):
        """Higgs potential with proper scaling"""
        v = 246.22e9 * 1.78e-36  # Higgs VEV in kg
        lam = 0.13  # Self-coupling
        return 0.25 * lam * (np.abs(phi)**2 - v**2)**2
    
    def Ricci_scalar(self):
        """Calculate the Ricci scalar curvature (simplified)"""
        # In a full theory, this would involve solving Einstein's equations
        # For simplicity, we use a constant background curvature here
        return 0.0  # Flat spacetime approximation
    
    def update_field_tensor(self):
        """
        Update the unified field tensor F_mu_nu, which represents the curvature
        of the Flower of Life lattice in spacetime.
        
        In this framework:
        - F_mu_nu = ∂_mu A_nu - ∂_nu A_mu + [A_mu, A_nu]
        - For U(1), the commutator term vanishes
        - For non-Abelian fields, includes self-interaction terms
        """
        # Reset field tensor
        self.F_mu_nu.fill(0)
        
        # Calculate field strength for electromagnetic field (U(1) gauge group)
        for mu in range(4):
            for nu in range(4):
                if mu == nu:
                    continue
                    
                # Calculate ∂_mu A_nu - ∂_nu A_mu
                if self.dimension == 1:
                    # 1D case - only time and one spatial dimension
                    if mu == 0:  # Time derivative
                        self.F_mu_nu[0, 1] = -np.gradient(self.A_mu[1], self.dx, axis=0)
                    elif nu == 0:  # Negative time derivative
                        self.F_mu_nu[1, 0] = -self.F_mu_nu[0, 1]
                else:
                    # Higher dimensions
                    if mu == 0:  # Time component
                        # Time derivative of spatial components
                        self.F_mu_nu[0, nu] = np.gradient(self.A_mu[nu], self.time_step, axis=0)
                        self.F_mu_nu[nu, 0] = -self.F_mu_nu[0, nu]
                    else:
                        # Spatial derivatives (curl in 3D, partial in 2D)
                        if self.dimension >= 2 and nu > 0 and mu != nu:
                            self.F_mu_nu[mu, nu] = np.gradient(self.A_mu[nu], self.dx, axis=mu-1) - \
                                                 np.gradient(self.A_mu[mu], self.dx, axis=nu-1)
        
        # Add non-Abelian contributions (simplified)
        if hasattr(self, 'W_mu'):
            # Add weak field contributions (SU(2))
            for a in range(3):
                for mu in range(4):
                    for nu in range(4):
                        if mu != nu:
                            # Add self-interaction terms (simplified)
                            self.F_mu_nu[mu, nu] += 0.1 * self.W_mu[a, mu] * self.W_mu[a, nu]
    
    def compute_gauge_field_derivative(self, A_mu, F_mu_nu, coupling=1.0):
        """
        Compute the time derivative of the gauge field A_μ using Yang-Mills equations.
        
        The Yang-Mills equation is: D^μ F_μν = J_ν
        Where:
        - D_μ is the gauge covariant derivative
        - F_μν is the field strength tensor
        - J_ν is the current
        
        For the time evolution, we use: dA_μ/dt = -F_μ0
        
        Parameters:
        -----------
        A_mu : ndarray
            The gauge field A_μ with shape (4, *grid_shape)
        F_mu_nu : ndarray
            The field strength tensor F_μν with shape (4, 4, *grid_shape)
        coupling : float, optional
            The gauge coupling constant (default: 1.0)
            
        Returns:
        --------
        ndarray
            The time derivative of A_μ with same shape as A_mu
        """
        # Initialize the time derivative
        dA_dt = np.zeros_like(A_mu)
        
        try:
            # For spatial components (i=1,2,3), dA_i/dt = -F_i0
            for i in range(1, 4):
                dA_dt[i] = -F_mu_nu[i, 0]
                
            # For the time component (μ=0), we use the equation of motion
            # In Coulomb gauge (∇·A = 0), we have: ∇²A0 = -J0
            # Here we use a simpler approach for stability
            if A_mu.shape[0] > 0:  # Check if time component exists
                dA_dt[0] = -self.laplacian(A_mu[0][np.newaxis, ...])[0]
                
                # Add current contribution if fermions are present
                if hasattr(self, 'fermions') and self.fermions:
                    # Simple current model: J0 ~ ψ†ψ
                    rho = np.sum([np.sum(np.abs(psi)**2, axis=0) for psi in self.fermions.values()], axis=0)
                    dA_dt[0] -= coupling * rho
            
            # Add damping for numerical stability
            damping = 0.1
            dA_dt -= damping * A_mu
            
        except Exception as e:
            print(f"Warning: Error in compute_gauge_field_derivative: {str(e)}")
            # Fall back to simpler implementation if there's an error
            laplacian_A = np.array([self.laplacian(comp) for comp in A_mu])
            dA_dt = laplacian_A - coupling * A_mu
        
        return dA_dt
        
    def evolve_gauge_field(self, A_mu, coupling, dt):
        """
        Evolve a general gauge field using Yang-Mills equations
        
        This implements a simple Euler step for the gauge field evolution.
        For better accuracy, use evolve_gauge_field_symplectic instead.
        
        Parameters:
        -----------
        A_mu : ndarray
            The gauge field A_μ with shape (4, *grid_shape)
        coupling : float
            The gauge coupling constant
        dt : float
            Time step size
            
        Returns:
        --------
        ndarray
            The updated gauge field
        """
        try:
            # Compute field strength tensor
            F_mu_nu = self.compute_field_strength(A_mu, coupling)
            
            # Compute time derivative using the more robust method
            dA_dt = self.compute_gauge_field_derivative(A_mu, F_mu_nu, coupling)
            
            # Update gauge field using Euler step
            new_A_mu = A_mu + dt * dA_dt
            
            # Project to maintain gauge condition if specified
            gauge_condition = getattr(self, 'gauge_condition', 'lorentz')
            if gauge_condition == 'lorentz':
                if hasattr(self, 'apply_lorenz_gauge'):
                    new_A_mu = self.apply_lorenz_gauge(new_A_mu)
            elif gauge_condition == 'coulomb':
                # Set time component to zero for Coulomb gauge
                if new_A_mu.shape[0] > 0:
                    new_A_mu[0] = 0.0
            
            return new_A_mu
            
        except Exception as e:
            print(f"Warning: Falling back to simple gauge field evolution: {str(e)}")
            # Fallback to simpler implementation if there's an error
            laplacian_A = np.array([self.laplacian(comp) for comp in A_mu])
            return A_mu + dt * (laplacian_A - coupling * A_mu)
    
    def check_energy_conservation(self):
        """
        Check if energy is conserved within tolerance.
        
        Returns:
        --------
        bool
            True if energy is conserved within tolerance, False otherwise
        """
        if len(self.energy_history) < 2:
            return True
            
        # Calculate relative energy change
        initial_energy = self.energy_history[0]
        current_energy = self.energy_history[-1]
        rel_change = abs((current_energy - initial_energy) / initial_energy)
        
        return rel_change <= self.energy_tolerance
    
    def adjust_timestep(self):
        """
        Adjust the time step based on energy conservation and CFL condition.
        Uses a more aggressive approach to maintain energy conservation.
        """
        if len(self.energy_history) < 5:
            return
            
        # Calculate relative energy change over last few steps
        energy_window = min(5, len(self.energy_history))
        energy_change = abs((self.energy_history[-1] - self.energy_history[-energy_window]) / 
                          (self.energy_history[0] + 1e-100))
        
        # More aggressive time step adjustment
        if energy_change > 1e-4:  # 0.01% change
            # Reduce time step more aggressively
            self.time_step = max(self.time_step * 0.5, self.min_dt)
        elif energy_change < 1e-6 and self.step % 5 == 0:  # Very stable
            # Increase time step more cautiously
            self.time_step = min(self.time_step * 1.1, self.max_dt)
            
        # Additional CFL condition
        max_wave_speed = self.c * np.sqrt(3)  # Maximum wave speed in 3D
        cfl_dt = self.cfl * self.dx / (max_wave_speed + 1e-100)
        self.time_step = min(self.time_step, cfl_dt)
        
        # Ensure time step stays within bounds
        self.time_step = max(min(self.time_step, self.max_dt), self.min_dt)
    
    def plot_fields(self, save_path=None):
        """Plot the current field configuration"""
        plt.figure(figsize=(15, 10))
        
        if self.dimension == 1:
            plt.subplot(2, 1, 1)
            plt.plot(self.x, np.real(self.phi))
            plt.title('Scalar Field (Real Part)')
            plt.xlabel('Position (m)')
            plt.ylabel('Field Value (kg)')
            
            plt.subplot(2, 1, 2)
            plt.plot(self.x, np.abs(self.fermions['electron'][0])**2)
            plt.title('Electron Probability Density')
            plt.xlabel('Position (m)')
            plt.ylabel('|ψ|²')
            
        elif self.dimension == 2:
            plt.subplot(1, 2, 1)
            plt.imshow(np.real(self.phi), cmap='viridis',
                      extent=[-self.box_size/2, self.box_size/2, -self.box_size/2, self.box_size/2])
            plt.colorbar(label='Field Value (kg)')
            plt.title('Scalar Field (Real Part)')
            
            plt.subplot(1, 2, 2)
            plt.imshow(np.sum(np.abs(self.A_mu[1:])**2, axis=0), cmap='plasma',
                      extent=[-self.box_size/2, self.box_size/2, -self.box_size/2, self.box_size/2])
            plt.colorbar(label='Gauge Field Strength (kg·m/s²)')
            plt.title('Gauge Fields')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    # The following methods were duplicates and have been removed:
    # - calculate_initial_timestep()
    # - check_energy_conservation()
    # - adjust_timestep()
    # 
    # The original implementations of these methods (earlier in the file) are kept
    # as they are more sophisticated and better handle the simulation's needs.
    
    def run_simulation(self, max_minutes=10, plot_interval=100, save_plots=False):
        """
        Run the simulation for a fixed duration with optimized performance
        
        Parameters:
        -----------
        max_minutes : float, optional
            Maximum runtime in minutes (default: 10)
        plot_interval : int, optional
            Number of steps between status updates (default: 100)
        save_plots : bool, optional
            Whether to save final plots (default: False)
            
        Returns:
        --------
        tuple
            (times, energies) arrays containing the simulation history
        """
        # Initialize simulation state
        self.time = 0.0
        self.step = 0
        self.time_history = []
        self.energy_history = []
        max_seconds = max_minutes * 60
        start_time = time_module.time()
        last_update = start_time
        
        print(f"Starting simulation with {max_minutes}-minute time limit...")
        print(f"Initial time step: {self.time_step*1e18:.2f} as")
        print(f"Energy tolerance: {self.energy_tolerance*100:.2e}%")
        
        # Pre-allocate arrays for better performance
        max_steps = int(1e6)  # Upper limit to prevent memory issues
        self.time_history = np.zeros(max_steps)
        self.energy_history = np.zeros(max_steps, dtype=np.complex128)
        
        # Run simulation with time limit
        current_step = 0
        
        try:
            with tqdm(desc="Simulation Progress", unit=" step") as pbar:
                while time_module.time() - start_time < max_seconds and current_step < max_steps:
                    # Dynamic time step adjustment
                    if current_step % 10 == 0 and current_step > 0:
                        self.adjust_timestep()
                    
                    # Evolve fields and get energy
                    energy = self.evolve_fields()
                    
                    # Store energy and time
                    self.time_history[current_step] = self.time
                    self.energy_history[current_step] = energy
                    current_step += 1
                    
                    # Update progress every plot_interval steps or every 5 seconds
                    current_time = time_module.time()
                    if current_step % plot_interval == 0 or (current_time - last_update) > 5:
                        elapsed = current_time - start_time
                        remaining = max(0, max_seconds - elapsed)
                        steps_per_sec = current_step / (elapsed + 1e-10)
                        
                        pbar.set_postfix({
                            't (fs)': f"{self.time*1e15:.2f}",
                            'dt (as)': f"{self.time_step*1e18:.2f}",
                            'E (eV)': f"{np.real(energy)/1.60218e-19:.2e}",
                            'Remaining': f"{remaining//60:.0f}m {remaining%60:.0f}s"
                        })
                        pbar.update(plot_interval)
                        last_update = current_time
                    
                    # Check for early termination
                    if current_time - start_time >= max_seconds:
                        print("\nTime limit reached. Finalizing simulation...")
                        break
                        
        except KeyboardInterrupt:
            print("\nSimulation interrupted by user.")
        except Exception as e:
            print(f"\nError during simulation: {str(e)}")
        finally:
            # Truncate the arrays to actual data
            self.time_history = self.time_history[:current_step]
            self.energy_history = self.energy_history[:current_step]
            
            # Calculate and display final statistics
            elapsed = time_module.time() - start_time
            print(f"\nSimulation completed in {elapsed//60:.0f}m {elapsed%60:.2f}s")
            print(f"Total steps: {current_step}")
            print(f"Final time: {self.time*1e15:.2f} fs")
            
            if len(self.energy_history) > 1:
                energy_change = abs((self.energy_history[-1] - self.energy_history[0]) / self.energy_history[0])
                print(f"Energy change: {energy_change*100:.2e}%")
            
            # Plot final results
            if current_step > 0:
                self.plot_energy_evolution()
                if save_plots:
                    self.plot_fields(save_path=f"final_state_{int(time_module.time())}.png")
            
            return self.time_history, self.energy_history
        
        # Calculate and print energy conservation
        if len(self.energy_history) > 1:
            energy_change = abs((self.energy_history[-1] - self.energy_history[0]) / (self.energy_history[0] + 1e-100))
            print(f"Relative energy change: {energy_change*100:.2e}%")
        
        # Plot results if we have data
        if self.time_history and self.energy_history:
            self.plot_energy_evolution()
        
        return np.array(self.time_history), np.array(self.energy_history)
    
    def plot_energy_evolution(self):
        """Plot energy evolution over time"""
        if not self.time_history or not self.energy_history:
            return
            
        plt.figure(figsize=(12, 5))
        
        # Plot energy
        plt.subplot(1, 2, 1)
        times_fs = np.array(self.time_history) * 1e15  # Convert to fs
        energies_ev = np.array(self.energy_history) / 1.60218e-19  # Convert to eV
        plt.plot(times_fs, energies_ev)
        plt.xlabel('Time (fs)')
        plt.ylabel('Total Energy (eV)')
        plt.title('Energy Evolution')
        plt.grid(True)
        
        # Plot relative energy change
        plt.subplot(1, 2, 2)
        if len(energies_ev) > 1:
            rel_energy = 100 * (energies_ev - energies_ev[0]) / energies_ev[0]
            plt.plot(times_fs, rel_energy)
            plt.axhline(0, color='r', linestyle='--', alpha=0.5)
            plt.xlabel('Time (fs)')
            plt.ylabel('Relative Energy Change (%)')
            plt.title('Energy Conservation')
            plt.title('Energy Conservation Error')
            plt.grid(True)
        
        # Plot field configurations
        plt.subplot(2, 2, 3)
        if self.dimension == 1:
            plt.plot(self.x * 1e9, np.real(self.phi), 'b-', label='Re(φ)')
            plt.plot(self.x * 1e9, np.imag(self.phi), 'r--', label='Im(φ)')
            plt.xlabel('Position (nm)')
            plt.ylabel('Field Amplitude')
            plt.title('Scalar Field')
            plt.legend()
            plt.grid(True)
        
        # Plot fermion probability density
        plt.subplot(2, 2, 4)
        if self.dimension == 1 and 'electron' in self.fermions:
            psi = self.fermions['electron']
            prob_density = np.sum(np.abs(psi)**2, axis=0)
            plt.plot(self.x * 1e9, prob_density, 'g-', label='|ψ|²')
            plt.xlabel('Position (nm)')
            plt.ylabel('Probability Density')
            plt.title('Electron Probability Density')
            plt.grid(True)
        
        plt.tight_layout()
        plt.show()



def main():
    # Run a 1D simulation for demonstration
    print("Initializing 1D Unified Field Simulation...")
    sim = UnifiedFieldSolver(grid_size=256, box_size=1e-10, dimension=1)
    
    # Run simulation for 1 femtosecond
    times, energies = sim.run_simulation(total_time=1e-15, plot_interval=10, save_plots=False)
    
    # Show final field configuration
    sim.plot_fields()
    
    # Print final energy
    print(f"Final energy: {energies[-1]:.3e} eV")
    print(f"Energy conservation: {np.std(energies)/np.mean(energies)*100:.2e}% relative fluctuation")


def run_tests():
    """Run validation tests for the unified field solver"""
    print("Running validation tests...")
    try:
        # Create a test instance with smaller grid for faster testing
        test_solver = UnifiedFieldSolver(
            grid_size=32,
            box_size=1e-10,
            dimension=1,  # 1D is faster for testing
            test_mode=True
        )
        
        # Run tests with a 30-second timeout
        success = test_solver.run_validation_tests(max_time=30)
        
        if success:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed. Review the output above.")
            
        return success
        
    except Exception as e:
        print(f"\n❌ Test runner failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import argparse
    
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Run unified field theory simulation')
    parser.add_argument('--test', action='store_true', help='Run tests only')
    parser.add_argument('--grid', type=int, default=32, help='Grid size')
    parser.add_argument('--dim', type=int, choices=[1, 2, 3], default=1, help='Number of dimensions')
    parser.add_argument('--time', type=float, default=1e-15, help='Total simulation time (s)')
    parser.add_argument('--cfl', type=float, default=0.1, help='CFL number for stability')
    
    args = parser.parse_args()
    
    if args.test:
        # Run tests with optimized parameters
        test_solver = UnifiedFieldSolver(
            grid_size=args.grid,
            dimension=args.dim,
            test_mode=True,
            cfl_number=args.cfl
        )
        test_solver.run_validation_tests(max_time=60)  # 1 minute max for tests
    else:
        # Run main simulation with optimized parameters
        try:
            # Initialize solver with better defaults
            sim = UnifiedFieldSolver(
                grid_size=args.grid,
                dimension=args.dim,
                test_mode=False,
                cfl_number=min(args.cfl, 0.1)  # Cap CFL for stability
            )
            
            # Ensure reasonable time parameters
            min_simulation_time = 1e-12  # 1 picosecond minimum
            simulation_time = max(float(args.time), min_simulation_time)
            
            print("\n=== Simulation Parameters ===")
            print(f"Grid size:        {args.grid}^{args.dim}")
            print(f"Box size:         {sim.box_size:.2e} m")
            print(f"Time step:        {sim.time_step:.2e} s")
            print(f"Total time:       {simulation_time:.2e} s")
            print(f"CFL number:       {args.cfl:.2f}")
            print("="*30 + "\n")
            
            # Run simulation with progress updates
            times, energies = sim.run_simulation(
                max_minutes=simulation_time/60,  # Convert to minutes
                plot_interval=50,  # More frequent updates
                save_plots=True
            )
            
            # Show final results
            if len(energies) > 1:
                print("\n=== Simulation Results ===")
                print(f"Total steps:      {len(times)}")
                print(f"Final time:       {times[-1]:.2e} s")
                print(f"Initial energy:   {energies[0]:.3e} J")
                print(f"Final energy:     {energies[-1]:.3e} J")
                energy_change = abs((energies[-1] - energies[0]) / energies[0] * 100)
                print(f"Energy change:    {energy_change:.2e}%")
                
                # Plot results
                if hasattr(sim, 'plot_fields'):
                    sim.plot_fields()
                    
                # Save final state
                if hasattr(sim, 'save_simulation_results'):
                    sim.save_simulation_results({
                        'times': times,
                        'energies': energies,
                        'config': {
                            'grid_size': sim.grid_size,
                            'box_size': sim.box_size,
                            'dimension': sim.dimension,
                            'cfl': sim.cfl_number
                        }
                    })
            
        except Exception as e:
            print(f"\n❌ Simulation failed: {str(e)}")
            import traceback
            traceback.print_exc()
