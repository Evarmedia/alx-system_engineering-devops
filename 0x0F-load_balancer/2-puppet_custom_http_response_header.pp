# Install HAProxy package
package { 'haproxy':
  ensure => installed,
}

# Define custom configuration for HAProxy
file { '/etc/haproxy/haproxy_custom.cfg':
  ensure  => present,
  content => @("EOF"
frontend http_front
    http-response set-header X-Served-By %H
EOF
),
  require => Package['haproxy'],
  notify  => Service['haproxy'],
}

# Include custom configuration in the HAProxy main configuration file
exec { 'include_custom_config':
  command => 'echo "import /etc/haproxy/haproxy_custom.cfg" >> /etc/haproxy/haproxy.cfg',
  creates => '/etc/haproxy/haproxy_custom.cfg',
  require => File['/etc/haproxy/haproxy_custom.cfg'],
  notify  => Service['haproxy'],
}

# Enable HAProxy init script
file { '/etc/default/haproxy':
  ensure  => present,
  content => "ENABLED=1",
  require => Package['haproxy'],
  notify  => Service['haproxy'],
}

# Restart HAProxy service
service { 'haproxy':
  ensure    => running,
  enable    => true,
  subscribe => [File['/etc/haproxy/haproxy_custom.cfg'], Exec['include_custom_config']],
}

